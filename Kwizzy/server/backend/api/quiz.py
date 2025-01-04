from flask_restful import Resource
from ..models import Quiz, Chapter, Question, Option
from flask_jwt_extended import jwt_required
from ..utils import role_required
from flask import request
from .. import db


class QuizApi(Resource):
    @jwt_required()
    def get(self, quiz_id=None):
        try:
            # Get specific quiz
            if quiz_id:
                quiz = Quiz.query.get_or_404(quiz_id)
                time_in_seconds = quiz.time_duration
                hours = time_in_seconds // 3600
                minutes = (time_in_seconds % 3600) // 60
                formatted_time = f"{hours:02d}:{minutes:02d}"
                return {
                    "id": quiz.id,
                    "name": quiz.name,
                    "description": quiz.description,
                    "price": quiz.price,
                    "chapter_id": quiz.chapter_id,
                    "time_duration": formatted_time,
                    "questions": [
                        {
                            "id": q.id,
                            "title": q.title,
                            "text": q.text,
                            "options": [
                                {
                                    "id": opt.id,
                                    "text": opt.text,
                                    "is_correct": (
                                        opt.is_correct
                                        if request.args.get("include_answers") == "true"
                                        else None
                                    ),
                                }
                                for opt in q.options
                            ],
                        }
                        for q in quiz.questions
                    ],
                }, 200

            # Get all quizzes with filters
            chapter_id = request.args.get("chapter_id")

            query = Quiz.query

            if chapter_id:
                query = query.filter(Quiz.chapter_id == chapter_id)
            quizzes = query.all()

            for quiz in quizzes:
                time_in_seconds = quiz.time_duration
                hours = time_in_seconds // 3600
                minutes = (time_in_seconds % 3600) // 60
                formatted_time = f"{hours:02d}:{minutes:02d}"
                quiz.time_duration = formatted_time

            return {
                "quizzes": [
                    {
                        "id": quiz.id,
                        "name": quiz.name,
                        "description": quiz.description,
                        "price": quiz.price,
                        "chapter_id": quiz.chapter_id,
                        "time_duration": quiz.time_duration,
                        "question_count": len(quiz.questions),
                    }
                    for quiz in quizzes
                ]
            }, 200

        except Exception as e:
            print("Error:", str(e))
            return {"message": "Error fetching quizzes", "error": str(e)}, 500

    @jwt_required()
    @role_required("admin")
    def post(self):
        try:
            data = request.get_json()
            if not data:
                return {"message": "No input data provided"}, 400

            # Validate required fields
            required_fields = [
                "name",
                "description",
                "chapter_id",
                "time_duration",
                "questions",
            ]
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return {
                    "message": f"Missing required fields: {', '.join(missing_fields)}"
                }, 400

            # Validate chapter exists
            chapter = Chapter.query.get(data["chapter_id"])
            if not chapter:
                return {"message": "Chapter not found"}, 404

            # conver time from hh:mm to seconds
            try:
                time_duration = data["time_duration"]
                hours, minutes = map(int, time_duration.split(":"))
                total_seconds = hours * 3600 + minutes * 60
            except ValueError:
                return {"message": "Invalid time format"}, 400

            # Create quiz
            new_quiz = Quiz(
                name=data["name"],
                description=data["description"],
                price=data.get("price", 0),
                chapter_id=data["chapter_id"],
                time_duration=total_seconds,
            )

            # Add questions and options
            for q_data in data["questions"]:
                question = Question(
                    title=q_data.get("title"), text=q_data["text"], quiz=new_quiz
                )

                # Validate at least one correct option
                has_correct = False
                for opt_data in q_data["options"]:
                    option = Option(
                        text=opt_data["text"],
                        is_correct=opt_data["is_correct"],
                        question=question,
                    )
                    if option.is_correct:
                        has_correct = True

                if not has_correct:
                    return {
                        "message": f"Question '{question.text}' must have at least one correct option"
                    }, 400

            db.session.add(new_quiz)
            db.session.commit()

            return {"message": "Quiz created successfully", "quiz_id": new_quiz.id}, 201

        except Exception as e:
            db.session.rollback()
            print("Error:", str(e))
            return {"message": "Error creating quiz", "error": str(e)}, 500

    @jwt_required()
    @role_required("admin")
    def put(self, quiz_id):
        try:
            quiz = Quiz.query.get_or_404(quiz_id)
            data = request.get_json()

            if not data:
                return {"message": "No input data provided"}, 400

            # Update basic quiz info
            if "name" in data:
                quiz.name = data["name"]
            if "description" in data:
                quiz.description = data["description"]
            if "price" in data:
                quiz.price = data["price"]
            if "time_duration" in data:
                try:
                    time_duration = data["time_duration"]
                    hours, minutes = map(int, time_duration.split(":"))
                    total_seconds = hours * 3600 + minutes * 60
                    quiz.time_duration = total_seconds
                except ValueError:
                    return {"message": "Invalid time format"}, 400
            if "chapter_id" in data:
                if not Chapter.query.get(data["chapter_id"]):
                    return {"message": "Chapter not found"}, 404
                quiz.chapter_id = data["chapter_id"]

            if "questions" in data:
                # Delete all existing questions and their options
                for question in quiz.questions:
                    db.session.delete(question)

                # Add new questions
                for q_data in data["questions"]:
                    question = Question(
                        title=q_data.get("title"), text=q_data["text"], quiz=quiz
                    )
                    db.session.add(question)

                    # Add options for this question
                    has_correct = False
                    for opt_data in q_data["options"]:
                        option = Option(
                            text=opt_data["text"],
                            is_correct=opt_data["is_correct"],
                            question=question,
                        )
                        db.session.add(option)
                        if option.is_correct:
                            has_correct = True

                    if not has_correct:
                        db.session.rollback()
                        return {
                            "message": f"Question '{question.text}' must have at least one correct option"
                        }, 400

            db.session.commit()
            return {"message": "Quiz updated successfully"}, 200

        except Exception as e:
            db.session.rollback()
            print("Error:", str(e))
            return {"message": "Error updating quiz", "error": str(e)}, 500

    @jwt_required()
    @role_required("admin")
    def delete(self, quiz_id):
        try:
            quiz = Quiz.query.get_or_404(quiz_id)

            # Check if quiz has been attempted
            if quiz.quiz_results:
                return {"message": "Cannot delete quiz with existing attempts"}, 400

            db.session.delete(quiz)
            db.session.commit()

            return {"message": "Quiz deleted successfully"}, 200

        except Exception as e:
            db.session.rollback()
            print("Error:", str(e))
            return {"message": "Error deleting quiz", "error": str(e)}, 500
