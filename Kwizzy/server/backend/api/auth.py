from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from backend.models import User
from backend import db
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
)
from datetime import datetime
from flask import current_app, request
from itsdangerous import URLSafeTimedSerializer
from ..tasks.celery_tasks import EmailService
import os
import logging

logger = logging.getLogger(__name__)


class Register(Resource):
    def post(self):
        # Get the JSON data from the request body
        data = request.get_json()

        # Destructure the required fields
        name = data.get("name")
        email = data.get("email")
        dob = data.get("dob")
        if dob:
            dob = datetime.strptime(dob, "%Y-%m-%d").date()
        qualification = data.get("qualification")
        role = data.get(
            "role", "student"
        )  # Default to 'student' if no role is provided
        password = data.get("password")
        profile_pic = data.get(
            "profile_pic", None
        )  # profile_pic is optional, can be None

        # Check if any required field is missing
        if not name or not email or not dob or not qualification or not password:
            return {"message": "Missing required fields"}, 400

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {"message": "User already exists"}, 400

        # Hash the password before storing it
        hashed_password = generate_password_hash(password)

        # Create a new user
        new_user = User(
            name=name,
            email=email,
            dob=dob,
            qualification=qualification,
            role=role,
            password=hashed_password,
            profile_pic=profile_pic,  # Can be None if not provided
        )

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User registered successfully!"}, 201


class Login(Resource):
    def post(self):
        # Get the JSON data from the request body
        data = request.get_json()

        # Destructure the data (assuming email and password are mandatory)
        email = data.get("email")
        password = data.get("password")

        # Validate required fields
        if not email or not password:
            return {"message": "Missing email or password"}, 400

        # Find the user by email
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return {"message": "Invalid credentials"}, 401

        additional_claims = {"role": user.role}

        # Create JWT tokens (access and refresh)
        access_token = create_access_token(
            identity=str(user.id), additional_claims=additional_claims
        )
        refresh_token = create_refresh_token(
            identity=str(user.id), additional_claims=additional_claims
        )

        return {
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_role": user.role,
            "user_id": user.id,
        }, 200


class ForgotPasswordAPI(Resource):
    def post(self):
        """Initiate password reset"""
        try:
            data = request.get_json()
            email = data.get("email")

            if not email:
                return {"error": "Email is required"}, 400

            user = User.query.filter_by(email=email).first()
            if not user:
                return {"error": "No account exists with this email address"}, 404

            # Generate reset token
            reset_token = generate_reset_token(user.id)

            # Create reset link
            reset_link = (
                f"{os.getenv('FRONTEND_URL')}/reset-password?token={reset_token}"
            )

            # Send email
            template_data = {
                "user_name": user.name,
                "reset_link": reset_link,
                "expiry_time": "1 hour",  # Token expiry time
            }

            EmailService.send_email(
                to_email=user.email,
                to_name=user.name,
                subject="Password Reset Request",
                template_name="password_reset.html",
                template_data=template_data,
            )

            return {"message": "Password reset link has been sent to your email"}, 200

        except Exception as e:
            logger.error(f"Password reset error: {str(e)}")
            return {"error": "Failed to process request"}, 500


class ResetPasswordAPI(Resource):
    def post(self):
        """Reset password using token"""
        try:
            data = request.get_json()
            token = data.get("token")
            new_password = data.get("new_password")

            if not token or not new_password:
                return {"error": "Token and new password are required"}, 400

            # Verify token and get user_id
            user_id = verify_reset_token(token)
            if not user_id:
                return {"error": "Invalid or expired token"}, 400

            user = User.query.get(user_id)
            if not user:
                return {"error": "User not found"}, 404

            # Update password
            user.password = generate_password_hash(new_password)
            db.session.commit()

            # Send confirmation email
            template_data = {
                "user_name": user.name,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            EmailService.send_email(
                to_email=user.email,
                to_name=user.name,
                subject="Password Reset Successful",
                template_name="password_reset_success.html",
                template_data=template_data,
            )

            return {"message": "Password reset successful"}, 200

        except Exception as e:
            logger.error(f"Password reset error: {str(e)}")
            return {"error": "Failed to reset password"}, 500


def generate_reset_token(user_id):
    """Generate a secure reset token"""
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(user_id, salt="password-reset-salt")


def verify_reset_token(token, expiration=3600):
    """Verify reset token"""
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        user_id = serializer.loads(
            token, salt="password-reset-salt", max_age=expiration
        )
        return user_id
    except:
        return None
