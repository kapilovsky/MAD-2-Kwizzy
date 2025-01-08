from flask_restful import Resource
from flask_jwt_extended import jwt_required
from ..utils import role_required, allowed_file
from ..models import User
from flask import request
from .. import db
import os
from flask import current_app as app
from werkzeug.utils import secure_filename


class UserApi(Resource):
    @jwt_required()
    def put(self, user_id):
        try:
            user = User.query.get_or_404(user_id)

            name = request.form.get("name")
            email = request.form.get("email")
            qualification = request.form.get("qualification")
            keep_existing_image = request.form.get("keep_existing_image") == "true"

            if not name or not email or not qualification:
                return {"message": "Name, email, and qualification are required"}, 400

            # Check if new email conflicts with existing users (excluding current user)
            existing_user = User.query.filter(
                User.email == email, User.id != user_id
            ).first()
            if existing_user:
                return {"message": "A user with this email already exists"}, 400

            user.name = name
            user.email = email
            user.qualification = qualification

            if "profile_pic" in request.files:
                file = request.files["profile_pic"]
                if file.filename != "":  # Check if file is actually selected
                    if not allowed_file(file.filename):
                        return {"message": "Invalid file type"}, 400

                    # Delete old profile picture if it exists
                    if user.profile_pic:
                        try:
                            old_image_path = os.path.join(
                                app.config["UPLOAD_FOLDER"],
                                "students",
                                user.profile_pic,
                            )
                            if os.path.exists(old_image_path):
                                os.remove(old_image_path)
                        except Exception as e:
                            print(f"Error removing old profile picture: {e}")

                    # Save new profile picture
                    upload_folder = os.path.join(
                        app.config["UPLOAD_FOLDER"], "students"
                    )
                    if not os.path.exists(upload_folder):
                        os.makedirs(upload_folder)

                    # Generate unique filename
                    filename = secure_filename(file.filename)
                    unique_filename = f"{user_id}_{filename}"
                    filepath = os.path.join(upload_folder, unique_filename)
                    file.save(filepath)

                    # Update user profile picture filename
                    user.profile_pic = unique_filename

            elif not keep_existing_image:
                # Remove existing profile picture if keep_existing_image is false
                if user.profile_pic:
                    try:
                        old_image_path = os.path.join(
                            app.config["UPLOAD_FOLDER"],
                            "students",
                            user.profile_pic,
                        )
                        if os.path.exists(old_image_path):
                            os.remove(old_image_path)
                    except Exception as e:
                        print(f"Error removing old profile picture: {e}")
                user.profile_pic = None

            db.session.commit()

            # Prepare response
            response_data = {
                "message": "Profile updated successfully",
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "qualification": user.qualification,
                    "profile_pic": user.profile_pic,
                    # Add any other user fields you want to return
                },
            }

            return response_data, 200

        except Exception as e:
            db.session.rollback()
            print("Error:", str(e))
            return {
                "message": "Error updating user profile",
                "error": str(e),
                "error_type": type(e).__name__,
            }, 400
