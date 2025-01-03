from flask_restful import Resource
from ..models import Chapter, Subject
from flask_jwt_extended import jwt_required
from ..utils import role_required
from flask import request
from .. import db
from sqlalchemy import desc


class ChapterApi(Resource):
    @jwt_required()
    @role_required("admin")
    def get(self, chapter_id=None):
        try:
            # Get a specific chapter
            if chapter_id:
                chapter = Chapter.query.get_or_404(chapter_id)
                return chapter.to_dict(), 200

            # Get all chapters with optional subject filter
            subject_id = request.args.get("subject_id")

            # Start with base query
            query = Chapter.query

            # Apply subject filter
            if subject_id:
                query = query.filter(Chapter.subject_id == subject_id)

            chapters = query.all()

            return {
                "chapters": [chapter.to_dict() for chapter in chapters],
                "total": len(chapters),
            }, 200

        except Exception as e:
            print("Error:", str(e))
            return {"message": "Error fetching chapters", "error": str(e)}, 500

    @jwt_required()
    @role_required("admin")
    def post(self):
        try:
            data = request.get_json()
            if not data:
                return {"message": "No input data provided"}, 400

            # Validate required fields
            required_fields = ["name", "description", "subject_id"]
            missing_fields = [field for field in required_fields if not data.get(field)]
            if missing_fields:
                return {
                    "message": "Missing required fields",
                    "fields": missing_fields,
                }, 400

            # Validate subject exists
            subject = Subject.query.get(data.get("subject_id"))
            if not subject:
                return {"message": "Subject not found"}, 404

            # Check if chapter name exists in the same subject
            existing_chapter = Chapter.query.filter_by(
                name=data.get("name"), subject_id=data.get("subject_id")
            ).first()

            if existing_chapter:
                return {
                    "message": "A chapter with this name already exists in this subject"
                }, 400

            # Create new chapter
            new_chapter = Chapter(
                name=data.get("name"),
                description=data.get("description"),
                subject_id=data.get("subject_id"),
            )

            db.session.add(new_chapter)
            db.session.commit()

            return {
                "message": "Chapter created successfully",
                "chapter": new_chapter.to_dict(),
            }, 201

        except Exception as e:
            db.session.rollback()
            print("Error:", str(e))
            return {"message": "Error creating chapter", "error": str(e)}, 500

    @jwt_required()
    @role_required("admin")
    def put(self, chapter_id):
        try:
            chapter = Chapter.query.get_or_404(chapter_id)
            data = request.get_json()

            if not data:
                return {"message": "No input data provided"}, 400

            # Validate required fields
            required_fields = ["name", "description"]
            missing_fields = [field for field in required_fields if not data.get(field)]
            if missing_fields:
                return {
                    "message": "Missing required fields",
                    "fields": missing_fields,
                }, 400

            # Check if new name conflicts with existing chapters in the same subject
            existing_chapter = Chapter.query.filter(
                Chapter.name == data.get("name"),
                Chapter.subject_id == chapter.subject_id,
                Chapter.id != chapter_id,
            ).first()

            if existing_chapter:
                return {
                    "message": "A chapter with this name already exists in this subject"
                }, 400

            # Update chapter
            chapter.name = data.get("name")
            chapter.description = data.get("description")

            # Update subject_id if provided
            if "subject_id" in data:
                if not Subject.query.get(data["subject_id"]):
                    return {"message": "Subject not found"}, 404
                chapter.subject_id = data["subject_id"]

            db.session.commit()

            return {
                "message": "Chapter updated successfully",
                "chapter": chapter.to_dict(),
            }, 200

        except Exception as e:
            db.session.rollback()
            print("Error:", str(e))
            return {"message": "Error updating chapter", "error": str(e)}, 500

    @jwt_required()
    @role_required("admin")
    def delete(self, chapter_id):
        try:
            chapter = Chapter.query.get_or_404(chapter_id)
            db.session.delete(chapter)
            db.session.commit()

            return {
                "message": "Chapter deleted successfully",
                "chapter_id": chapter_id,
            }, 200

        except Exception as e:
            db.session.rollback()
            print("Error:", str(e))
            return {"message": "Error deleting chapter", "error": str(e)}, 500
