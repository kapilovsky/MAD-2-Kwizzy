# user_answer_api.py
from flask_restful import Resource
from ..models import UserAnswer, QuizResult, Question, Option, Quiz
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from .. import db, cache
from time import perf_counter_ns
from ..utils import IndianTimeZone


class UserAnswerApi(Resource):
    def __init__(self):
        self.cache_timeout = 300

    @jwt_required()
    def post(self):
        """
        Expected request format:
        {
            "quiz_id": 1,
            "answers": [
                {
                    "question_id": 1,
                    "selected_option_id": 2
                },
                ...
            ]
        }
        """
        try:
            data = request.get_json()
            user_id = get_jwt_identity()

            # Validate request data
            if not data or "quiz_id" not in data or "answers" not in data:
                return {"message": "Invalid request format"}, 400

            quiz = Quiz.query.get_or_404(data["quiz_id"])
            if not quiz.is_available():
                return (
                    {
                        "message": "Quiz is not available",
                        "deadline": (
                            quiz.deadline.strftime("%Y-%m-%d %H:%M")
                            if quiz.deadline
                            else None
                        ),
                    }
                ), 403

            if quiz.one_attempt_only and quiz.has_attempted(user_id):
                return (
                    {
                        "message": "Quiz can be attempted only once",
                    }
                ), 403

            # Calculate results
            total_questions = len(quiz.questions)
            correct_answers = 0
            user_answers = []

            # Process each answer
            for answer in data["answers"]:
                question_id = answer.get("question_id")
                selected_option_id = answer.get("selected_option_id")

                if not question_id or not selected_option_id:
                    continue

                # Get the correct option for this question
                question = Question.query.get(question_id)
                if not question or question.quiz_id != quiz.id:
                    return {"message": f"Invalid question_id: {question_id}"}, 400

                correct_option = Option.query.filter_by(
                    question_id=question_id, is_correct=True
                ).first()

                is_correct = correct_option and correct_option.id == selected_option_id
                if is_correct:
                    correct_answers += 1

                user_answers.append(
                    {
                        "question_id": question_id,
                        "selected_option": selected_option_id,
                        "is_correct": is_correct,
                    }
                )

            # Calculate percentage
            percentage = (
                (correct_answers / total_questions) * 100 if total_questions > 0 else 0
            )

            # Create quiz result
            quiz_result = QuizResult(
                quiz_id=quiz.id,
                user_id=user_id,
                marks_scored=correct_answers,
                total_marks=total_questions,
                completed_at=IndianTimeZone(),
            )

            db.session.add(quiz_result)
            db.session.flush()  # Get the ID of quiz_result

            # Create user answers
            for answer in user_answers:
                user_answer = UserAnswer(
                    result_id=quiz_result.id,
                    question_id=answer["question_id"],
                    selected_option=answer["selected_option"],
                    is_correct=answer["is_correct"],
                )
                db.session.add(user_answer)

            db.session.commit()

            # Prepare detailed result response
            result = {
                "quiz_id": quiz.id,
                "quiz_name": quiz.name,
                "quiz_description": quiz.description,
                "total_questions": total_questions,
                "marks_scored": correct_answers,
                "total_marks": total_questions,
                "percentage": round(percentage, 2),
                "result_id": quiz_result.id,
                "completed_at_formatted": quiz_result.completed_at.strftime(
                    "%d-%m-%Y %I:%M:%S %p IST"
                ),  # Add formatted date
                "user_answers": [  # Rename detailed_answers to user_answers for consistency
                    {
                        "id": idx + 1,  # Add an ID for each answer
                        "question_id": answer["question_id"],
                        "selected_option": answer["selected_option"],
                        "is_correct": answer["is_correct"],
                        "correct_option": Option.query.filter_by(
                            question_id=answer["question_id"], is_correct=True
                        )
                        .first()
                        .id,
                    }
                    for idx, answer in enumerate(user_answers)
                ],
            }

            return {"message": "Quiz submitted successfully", "result": result}, 201

        except Exception as e:
            db.session.rollback()
            return {"message": f"Error submitting quiz: {str(e)}"}, 500

    @jwt_required()
    def put(self, answer_id):
        try:
            user_id = get_jwt_identity()
            answer = UserAnswer.query.get_or_404(answer_id)

            # Verify user owns this answer
            if answer.quiz_result.user_id != user_id:
                return {"message": "Unauthorized access"}, 403

            data = request.get_json()

            if "selected_option" in data:
                answer.selected_option = data["selected_option"]
            if "is_correct" in data:
                answer.is_correct = data["is_correct"]

            db.session.commit()
            self.invalidate_cache()

            return answer.to_dict(), 200

        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 400

    @jwt_required()
    def delete(self, answer_id):
        try:
            user_id = get_jwt_identity()
            answer = UserAnswer.query.get_or_404(answer_id)

            # Verify user owns this answer
            if answer.quiz_result.user_id != user_id:
                return {"message": "Unauthorized access"}, 403

            db.session.delete(answer)
            db.session.commit()
            self.invalidate_cache()

            return {"message": "Answer deleted successfully"}, 200

        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 400

    def invalidate_cache(self):
        """Invalidate all user answer related caches"""
        cache.delete_memoized(self.get_user_answer_by_id)
        cache.delete_memoized(self.get_result_answers)

    def get_question_details(self, question_id):
        """Helper method to get question details including correct answer"""
        question = Question.query.get_or_404(question_id)
        correct_option = Option.query.filter_by(
            question_id=question_id, is_correct=True
        ).first()

        return {
            "question_text": question.text,
            "correct_option_id": correct_option.id if correct_option else None,
            "correct_option_text": correct_option.text if correct_option else None,
        }
