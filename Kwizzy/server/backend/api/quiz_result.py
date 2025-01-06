# quiz_result_api.py
from flask_restful import Resource
from ..models import QuizResult, UserAnswer
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from .. import db, cache
from time import perf_counter_ns
from sqlalchemy import or_


class QuizResultApi(Resource):
    def __init__(self):
        self.cache_timeout = 300

    @cache.memoize(timeout=300)
    def get_quiz_result_by_id(self, result_id):
        """Cached method to get single quiz result"""
        quiz_result = QuizResult.query.get_or_404(result_id)
        return quiz_result.to_dict()

    @cache.memoize(timeout=300)
    def get_user_quiz_results(self, user_id):
        """Cached method to get all quiz results for a user"""
        results = QuizResult.query.filter_by(user_id=user_id).all()
        return [result.to_dict() for result in results]

    @jwt_required()
    def get(self, result_id=None):
        try:
            user_id = get_jwt_identity()

            if result_id:
                result = QuizResult.query.get_or_404(result_id)
                # Ensure user can only access their own results
                if result.user_id != user_id:
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
            db.session.flush()  # Get the ID of new_result

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
            self.invalidate_cache()

            return {
                "message": "Quiz result created successfully",
                "result": new_result.to_dict(),
            }, 201

        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 400

    def invalidate_cache(self):
        """Invalidate all quiz result related caches"""
        cache.delete_memoized(self.get_quiz_result_by_id)
        cache.delete_memoized(self.get_user_quiz_results)
