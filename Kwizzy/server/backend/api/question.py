from flask_restful import Resource
from ..models import Quiz, Chapter, Question, Option
from flask_jwt_extended import jwt_required
from ..utils import role_required
from flask import request
from .. import db


class QuestionApi(Resource):
    @jwt_required()
    @role_required("admin")
    def post(self, quiz_id):
        try:
            quiz = Quiz.query.get_or_404(quiz_id)
            data = request.get_json()

            if not data:
                return {"message": "No input data provided"}, 400

            # Validate required fields
            required_fields = ["text", "options"]
            if not all(field in data for field in required_fields):
                return {"message": "Missing required fields"}, 400

            # Create question
            question = Question(
                title=data.get("title"), text=data["text"], quiz_id=quiz.id
            )

            # Add options
            has_correct = False
            for opt_data in data["options"]:
                option = Option(
                    text=opt_data["text"],
                    is_correct=opt_data["is_correct"],
                    question=question,
                )
                if option.is_correct:
                    has_correct = True

            if not has_correct:
                return {
                    "message": "Question must have at least one correct option"
                }, 400

            db.session.add(question)
            db.session.commit()

            return {
                "message": "Question added successfully",
                "question_id": question.id,
            }, 201

        except Exception as e:
            db.session.rollback()
            print("Error:", str(e))
            return {"message": "Error adding question", "error": str(e)}, 500

    @jwt_required()
    @role_required("admin")
    def delete(self, quiz_id, question_id):
        try:
            question = Question.query.filter_by(
                quiz_id=quiz_id, id=question_id
            ).first_or_404()
            db.session.delete(question)
            db.session.commit()

            return {"message": "Question deleted successfully"}, 200

        except Exception as e:
            db.session.rollback()
            print("Error:", str(e))
            return {"message": "Error deleting question", "error": str(e)}, 500
