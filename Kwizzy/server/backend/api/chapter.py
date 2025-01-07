from flask_restful import Resource
from ..models import Chapter, Subject
from flask_jwt_extended import jwt_required
from ..utils import role_required
from flask import request
from .. import db
from sqlalchemy import desc
from time import perf_counter_ns


class ChapterApi(Resource):

    def get_chapter_by_id(self, chapter_id):
        chapter = Chapter.query.get_or_404(chapter_id)
        return chapter.to_dict()

    def get_chapters_by_subject(self, subject_id):
        chapters = Chapter.query.filter(Chapter.subject_id == subject_id).all()
        return [chapter.to_dict() for chapter in chapters]

    def get_all_chapters(self):
        start = perf_counter_ns()
        chapters = Chapter.query.all()
        end = perf_counter_ns()
        print(f"Time taken to fetch chapters: {(end - start) / 1_000_000} ms")
        return [chapter.to_dict() for chapter in chapters]

    @jwt_required()
    def get(self, chapter_id=None):
        try:
            # Get a specific chapter
            if chapter_id:
                return self.get_chapter_by_id(chapter_id), 200

            # Get chapters with optional subject filter
            subject_id = request.args.get("subject_id")

            if subject_id:
                chapters = self.get_chapters_by_subject(subject_id)
            else:
                chapters = self.get_all_chapters()

            return {"chapters": chapters, "total": len(chapters)}, 200

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

            # Log received data
            print("Received data:", data)

            # Validate required fields
            required_fields = ["name", "description", "subject_id"]
            missing_fields = [field for field in required_fields if not data.get(field)]
            if missing_fields:
                return {
                    "message": f"Missing required fields: {', '.join(missing_fields)}",
                    "fields": missing_fields,
                }, 400

            # Validate subject exists
            subject = Subject.query.get(data.get("subject_id"))
            if not subject:
                return {
                    "message": f"Subject with ID {data.get('subject_id')} not found"
                }, 404

            # Check for duplicate chapter name
            existing_chapter = Chapter.query.filter_by(
                name=data.get("name"), subject_id=data.get("subject_id")
            ).first()
            if existing_chapter:
                return {
                    "message": f"A chapter named '{data.get('name')}' already exists in this subject"
                }, 400

            # Create new chapter
            new_chapter = Chapter(
                name=data.get("name"),
                description=data.get("description"),
                subject_id=data.get("subject_id"),
            )

            db.session.add(new_chapter)
            db.session.commit()

            # Refresh the chapter to ensure all fields are loaded
            db.session.refresh(new_chapter)

            response_data = {
                "message": "Chapter created successfully",
                "chapter": new_chapter.to_dict(),
            }

            # Log response data
            print("Sending response:", response_data)

            return response_data, 201

        except Exception as e:
            db.session.rollback()
            print("Error creating chapter:", str(e))
            print("Error type:", type(e).__name__)
            import traceback

            traceback.print_exc()

            return {
                "message": "Error creating chapter",
                "error": str(e),
                "error_type": type(e).__name__,
            }, 500

    @jwt_required()
    @role_required("admin")
    def put(self, chapter_id):
        try:
            chapter = Chapter.query.get_or_404(chapter_id)
            original_subject_id = chapter.subject_id
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

            # Check for duplicate chapter name
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

            # Update subject if provided
            new_subject_id = data.get("subject_id")
            if new_subject_id:
                if not Subject.query.get(new_subject_id):
                    return {"message": "Subject not found"}, 404
                chapter.subject_id = new_subject_id

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
