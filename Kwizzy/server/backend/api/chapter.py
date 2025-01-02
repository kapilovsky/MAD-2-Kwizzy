from flask_restful import Resource
from ..models import Chapter
from flask_jwt_extended import jwt_required
from ..utils import role_required
from flask import request
from .. import db


class ChapterApi(Resource):
    @jwt_required()
    @role_required("admin")
    def get(self):
        search_query = request.args.get("search_query", "").strip()
        if search_query:
            chapter_list = Chapter.query.filter(
                Chapter.name.ilike(f"%{search_query}%")
            ).all()
        else:
            chapter_list = Chapter.query.all()
        return {
            "chapters": list(map(lambda chapter: chapter.to_dict(), chapter_list)),
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

            required_fields = ["name", "description", "subject_id"]
            for field in required_fields:
                if not data.get(field):
                    return {"message": f"{field.capitalize()} is required"}, 400

            # Check if chapter exists
            existing_chapter = Chapter.query.filter_by(name=data.get("name")).first()
            if existing_chapter:
                return {"message": "A chapter with this name already exists"}, 400

            # Create new chapter
            new_chapter = Chapter(
                name=data.get("name"),
                description=data.get("description"),
                subject_id=data.get("subject_id"),
            )

            print("Creating chapter:", new_chapter.to_dict())  # Debug print

            db.session.add(new_chapter)
            db.session.commit()

            return {"message": "Chapter created successfully"}, 201
        except Exception as e:
            db.session.rollback()
            print("Error:", str(e))
            return {"message": "An error occurred while creating the chapter"}, 500
