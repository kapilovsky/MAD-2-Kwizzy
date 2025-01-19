# quiz_result_api.py
from flask_restful import Resource
from ..models import QuizResult, UserAnswer
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from .. import db
from sqlalchemy.orm import joinedload


class QuizResultApi(Resource):
    def get_quiz_result_by_id(self, result_id):
        try:
            # Use joinedload to load relationships efficiently
            quiz_result = QuizResult.query.options(
                joinedload(QuizResult.quiz),
                joinedload(QuizResult.user_answers).joinedload(
                    UserAnswer.selected_option_rel
                ),
            ).get_or_404(result_id)
            return quiz_result.to_dict()
        except Exception as e:
            return ({"error": f"Error fetching quiz result: {str(e)}"}), 500

    def get_user_quiz_results(self, user_id):
        results = QuizResult.query.filter_by(user_id=user_id).all()
        return [result.to_dict() for result in results]

    @jwt_required()
    def get(self, result_id=None):
        try:
            user_id = get_jwt_identity()
            user_id = int(user_id)

            if result_id:
                result = QuizResult.query.get_or_404(result_id)
                # Ensure user can only access their own results
                if int(result.user_id) != user_id:
                    return {"message": "Unauthorized access"}, 403
                return self.get_quiz_result_by_id(result_id)

            return {"results": self.get_user_quiz_results(user_id)}

        except Exception as e:
            return {"message": str(e)}, 500

    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            user_id = get_jwt_identity()

            required_fields = ["quiz_id", "answers"]
            for field in required_fields:
                if field not in data:
                    return {"message": f"{field} is required"}, 400

            # Create quiz result
            new_result = QuizResult(
                quiz_id=data["quiz_id"],
                user_id=user_id,
                marks_scored=data.get("marks_scored"),
                total_marks=data.get("total_marks"),
            )

            db.session.add(new_result)
            db.session.flush()

            # Create user answers
            for answer in data["answers"]:
                user_answer = UserAnswer(
                    result_id=new_result.id,
                    question_id=answer["question_id"],
                    selected_option=answer.get("selected_option"),
                    is_correct=answer.get("is_correct", False),
                )
                db.session.add(user_answer)

            db.session.commit()

            return {
                "message": "Quiz result created successfully",
                "result": new_result.to_dict(),
            }, 201

        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 400
