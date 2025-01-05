from flask_restful import Resource
from ..models import Subject
from flask_jwt_extended import jwt_required
from ..utils import role_required, allowed_file
from flask import request
from .. import db
import os
from flask import current_app as app
from werkzeug.utils import secure_filename
from sqlalchemy import or_
from .. import cache
from time import perf_counter_ns


class SubjectApi(Resource):

    def __init__(self):
        self.cache_timeout = 300

    @cache.cached(timeout=300, key_prefix="all_subjects")
    def get_all_subjects(self):
        """Cached method to get all subjects"""
        start = perf_counter_ns()
        subject_list = Subject.query.all()
        end = perf_counter_ns()
        print(f"Time taken to fetch subjects: {(end - start) / 1_000_000} ms")
        return [subject.to_dict() for subject in subject_list]

    @cache.memoize(timeout=300)
    def get_subject_by_id(self, subject_id):
        """Cached method to get single subject"""
        subject = Subject.query.get_or_404(subject_id)
        return subject.to_dict()

    @cache.memoize(timeout=300)
    def search_subjects(self, search_query):
        """Cached method to search subjects"""
        subjects = Subject.query.filter(
            or_(
                Subject.name.ilike(f"%{search_query}%"),
                Subject.description.ilike(f"%{search_query}%"),
            )
        ).all()
        return [subject.to_dict() for subject in subjects]

    @jwt_required()
    @role_required("admin")
    def get(self, subject_id=None):
        try:
            search_query = request.args.get("search", "").lower()

            if search_query:
                return {"subjects": self.search_subjects(search_query)}

            if subject_id:
                if not Subject.query.get(subject_id):
                    return {"message": "Subject not found"}, 404
                return self.get_subject_by_id(subject_id)

            return {"subjects": self.get_all_subjects()}

        except Exception as e:
            return {"message": str(e)}, 500

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

            self.invalidate_cache()
            return (
                {
                    "message": "Subject created successfully",
                    "subject": new_subject.to_dict(),
                }
            ), 201

        except Exception as e:
            db.session.rollback()
            print("Error:", str(e))  # Debug print
            return {
                "message": "Error creating subject",
                "error": str(e),
                "error_type": type(e).__name__,
            }, 400

    @jwt_required()
    @role_required("admin")
    def delete(self, subject_id):
        try:
            subject = Subject.query.get_or_404(subject_id)

            # Delete the associated image file if it exists
            if subject.subject_image:
                image_path = os.path.join(
                    app.config["UPLOAD_FOLDER"], subject.subject_image
                )
                if os.path.exists(image_path):
                    os.remove(image_path)

            db.session.delete(subject)
            db.session.commit()
            self.invalidate_cache()
            return {"message": "Subject deleted successfully"}, 200

        except Exception as e:
            db.session.rollback()
            print("Error:", str(e))
            return {
                "message": "Error deleting subject",
                "error": str(e),
                "error_type": type(e).__name__,
            }, 400

    @jwt_required()
    @role_required("admin")
    def put(self, subject_id):
        cache.clear()
        try:
            subject = Subject.query.get_or_404(subject_id)

            # Get form data
            name = request.form.get("name")
            description = request.form.get("description")
            image = request.files.get("image")

            # Validate required fields
            if not name or not description:
                return {"message": "Name and description are required"}, 400

            # Check if new name conflicts with existing subjects (excluding current subject)
            existing_subject = Subject.query.filter(
                Subject.name == name, Subject.id != subject_id
            ).first()
            if existing_subject:
                return {"message": "A subject with this name already exists"}, 400

            # Handle image upload if new image is provided
            if image:
                if not allowed_file(image.filename):
                    return {"message": "Invalid file type"}, 400

                # Delete old image if it exists
                if subject.subject_image:
                    old_image_path = os.path.join(
                        app.config["UPLOAD_FOLDER"], subject.subject_image
                    )
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)

                # Save new image
                filename = secure_filename(image.filename)
                upload_folder = app.config["UPLOAD_FOLDER"]
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                filepath = os.path.join(upload_folder, filename)
                image.save(filepath)

                # Update subject image filename
                subject.subject_image = filename

            # Update subject details
            subject.name = name
            subject.description = description

            db.session.commit()
            self.invalidate_cache()
            return subject.to_dict(), 200

        except Exception as e:
            db.session.rollback()
            print("Error:", str(e))
            return {
                "message": "Error updating subject",
                "error": str(e),
                "error_type": type(e).__name__,
            }, 400

    def invalidate_cache(self):
        """Invalidate all subject-related caches"""
        cache.delete("all_subjects")
        cache.delete_memoized(self.get_subject_by_id)
        cache.delete_memoized(self.search_subjects)
