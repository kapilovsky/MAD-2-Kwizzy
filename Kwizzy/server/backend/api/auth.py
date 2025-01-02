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
        }, 200
