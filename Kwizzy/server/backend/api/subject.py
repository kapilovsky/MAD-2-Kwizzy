from flask_restful import Resource
from ..models import Subject
from flask_jwt_extended import jwt_required
from ..utils import role_required, allowed_file
from flask import request
from .. import db
import os
from flask import current_app as app
from werkzeug.utils import secure_filename


class SubjectApi(Resource):
    @jwt_required()
    @role_required("admin")
    def get(self):
        search_query = request.args.get("search_query", "").strip()
        if search_query:
            subject_list = Subject.query.filter(
                Subject.name.ilike(f"%{search_query}%")
            ).all()
        else:
            subject_list = Subject.query.all()
        return {
            "subjects": list(map(lambda subject: subject.to_dict(), subject_list)),
            "search_query": search_query,
        }

    @jwt_required()
    @role_required("admin")
    def post(self):
        try:
            name = request.form.get("name")
            description = request.form.get("description")
            image = request.files.get("image")
            data = request.form

            required_fields = ["name", "description"]
            for field in required_fields:
                if not data.get(field):
                    return {"message": f"{field.capitalize()} is required"}, 400

            # Check if subject exists
            existing_subject = Subject.query.filter_by(name=data.get("name")).first()
            if existing_subject:
                return {"message": "A subject with this name already exists"}, 400

            if image and allowed_file(image.filename):
                upload_folder = app.config["UPLOAD_FOLDER"]
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                filename = secure_filename(image.filename)
                filepath = os.path.join(upload_folder, filename)
                image.save(filepath)
            else:
                return {"message": "Invalid file type or no file uploaded"}, 400

            # Create new subject
            new_subject = Subject(
                name=name,
                description=description,
                subject_image=filename,
            )

            print("Creating subject:", new_subject.to_dict())  # Debug print

            db.session.add(new_subject)
            db.session.commit()

            print("Subject created successfully")  # Debug print
            return new_subject.to_dict(), 201

        except Exception as e:
            db.session.rollback()
            print("Error:", str(e))  # Debug print
            return {
                "message": "Error creating subject",
                "error": str(e),
                "error_type": type(e).__name__,
            }, 400
