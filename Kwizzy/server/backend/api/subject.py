from flask_restful import Resource
from ..models import Subject
from flask_jwt_extended import jwt_required
from ..utils import role_required
from flask import request
from .. import db


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
            data = request.get_json()
            print("Received data:", data)  # Debug print

            if not data:
                return {"message": "No input data provided"}, 400

            required_fields = ["name", "description"]
            for field in required_fields:
                if not data.get(field):
                    return {"message": f"{field.capitalize()} is required"}, 400

            # Check if subject exists
            existing_subject = Subject.query.filter_by(name=data.get("name")).first()
            if existing_subject:
                return {"message": "A subject with this name already exists"}, 400

            # Create new subject
            new_subject = Subject(
                name=data.get("name"),
                description=data.get("description"),
                subject_image=data.get("subject_image"),
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
