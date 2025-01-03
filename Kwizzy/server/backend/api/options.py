# options.py
from flask_restful import Resource
from ..models import Option, Question, Quiz
from flask_jwt_extended import jwt_required
from ..utils import role_required
from flask import request
from .. import db


class OptionApi(Resource):
    @jwt_required()
    def get(self, question_id=None, option_id=None):
        try:
            # Get specific option
            if option_id:
                option = Option.query.get_or_404(option_id)
                return {
                    "id": option.id,
                    "text": option.text,
                    "is_correct": (
                        option.is_correct
                        if request.args.get("include_answers") == "true"
                        else None
                    ),
                    "question_id": option.question_id,
                }, 200

            # Get all options for a question
            if question_id:
                question = Question.query.get_or_404(question_id)
                return {
                    "options": [
                        {
                            "id": opt.id,
                            "text": opt.text,
                            "is_correct": (
                                opt.is_correct
                                if request.args.get("include_answers") == "true"
                                else None
                            ),
                            "question_id": opt.question_id,
                        }
                        for opt in question.options
                    ]
                }, 200

            return {"message": "Question ID is required"}, 400

        except Exception as e:
            print("Error:", str(e))
            return {"message": "Error fetching options", "error": str(e)}, 500

    @jwt_required()
    @role_required("admin")
    def post(self, question_id):
        try:
            question = Question.query.get_or_404(question_id)
            data = request.get_json()

            if not data:
                return {"message": "No input data provided"}, 400

            # Validate required fields
            if "text" not in data:
                return {"message": "Option text is required"}, 400

            # Create new option
            new_option = Option(
                text=data["text"],
                is_correct=data.get("is_correct", False),
                question_id=question_id,
            )

            # If this is marked as correct, validate against other options
            if new_option.is_correct:
                # Check if this question already has a correct answer
                existing_correct = Option.query.filter_by(
                    question_id=question_id, is_correct=True
                ).first()

                # If multiple correct answers aren't allowed, return error
                if existing_correct and not data.get("allow_multiple_correct"):
                    return {
                        "message": "This question already has a correct answer. Set allow_multiple_correct=true to allow multiple correct answers"
                    }, 400

            db.session.add(new_option)
            db.session.commit()

            return {
                "message": "Option created successfully",
                "option": {
                    "id": new_option.id,
                    "text": new_option.text,
                    "is_correct": new_option.is_correct,
                    "question_id": new_option.question_id,
                },
            }, 201

        except Exception as e:
            db.session.rollback()
            print("Error:", str(e))
            return {"message": "Error creating option", "error": str(e)}, 500

    @jwt_required()
    @role_required("admin")
    def put(self, option_id):
        try:
            option = Option.query.get_or_404(option_id)
            data = request.get_json()

            if not data:
                return {"message": "No input data provided"}, 400

            # Update text if provided
            if "text" in data:
                option.text = data["text"]

            # Update is_correct if provided
            if "is_correct" in data:
                # If marking as correct, check other options
                if data["is_correct"] and not data.get("allow_multiple_correct"):
                    existing_correct = (
                        Option.query.filter_by(
                            question_id=option.question_id, is_correct=True
                        )
                        .filter(Option.id != option_id)
                        .first()
                    )

                    if existing_correct:
                        return {
                            "message": "This question already has a correct answer. Set allow_multiple_correct=true to allow multiple correct answers"
                        }, 400

                option.is_correct = data["is_correct"]

                # Ensure at least one correct option remains
                if not option.is_correct:
                    correct_options = Option.query.filter_by(
                        question_id=option.question_id, is_correct=True
                    ).count()

                    if correct_options == 0:
                        return {
                            "message": "Cannot remove last correct option. Question must have at least one correct answer"
                        }, 400

            db.session.commit()

            return {
                "message": "Option updated successfully",
                "option": {
                    "id": option.id,
                    "text": option.text,
                    "is_correct": option.is_correct,
                    "question_id": option.question_id,
                },
            }, 200

        except Exception as e:
            db.session.rollback()
            print("Error:", str(e))
            return {"message": "Error updating option", "error": str(e)}, 500

    @jwt_required()
    @role_required("admin")
    def delete(self, option_id):
        try:
            option = Option.query.get_or_404(option_id)

            # Check if this is the last option
            option_count = Option.query.filter_by(
                question_id=option.question_id
            ).count()

            if option_count <= 2:  # Assuming you want at least 2 options per question
                return {
                    "message": "Cannot delete option. Question must have at least 2 options"
                }, 400

            # Check if this is the last correct option
            if option.is_correct:
                correct_options = Option.query.filter_by(
                    question_id=option.question_id, is_correct=True
                ).count()

                if correct_options <= 1:
                    return {
                        "message": "Cannot delete the only correct option. Question must have at least one correct answer"
                    }, 400

            db.session.delete(option)
            db.session.commit()

            return {"message": "Option deleted successfully"}, 200

        except Exception as e:
            db.session.rollback()
            print("Error:", str(e))
            return {"message": "Error deleting option", "error": str(e)}, 500


class OptionsBulkApi(Resource):
    @jwt_required()
    @role_required("admin")
    def post(self, question_id):
        """Add multiple options to a question at once"""
        try:
            question = Question.query.get_or_404(question_id)
            data = request.get_json()

            if not data or "options" not in data:
                return {"message": "No options provided"}, 400

            options_data = data["options"]
            if not isinstance(options_data, list):
                return {"message": "Options must be provided as a list"}, 400

            # Validate at least one correct answer
            has_correct = False
            for opt_data in options_data:
                if opt_data.get("is_correct"):
                    has_correct = True
                    break

            if not has_correct:
                return {"message": "At least one option must be marked as correct"}, 400

            # Create all options
            new_options = []
            for opt_data in options_data:
                if "text" not in opt_data:
                    return {"message": "Each option must have text"}, 400

                option = Option(
                    text=opt_data["text"],
                    is_correct=opt_data.get("is_correct", False),
                    question_id=question_id,
                )
                db.session.add(option)
                new_options.append(option)

            db.session.commit()

            return {
                "message": "Options created successfully",
                "options": [
                    {
                        "id": opt.id,
                        "text": opt.text,
                        "is_correct": opt.is_correct,
                        "question_id": opt.question_id,
                    }
                    for opt in new_options
                ],
            }, 201

        except Exception as e:
            db.session.rollback()
            print("Error:", str(e))
            return {"message": "Error creating options", "error": str(e)}, 500
