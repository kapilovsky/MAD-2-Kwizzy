from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    current_app,
    abort,
)
from .models import User, Subject, Chapter, Quiz, Question, Option, QuizResult
from . import db
from flask_login import login_required, current_user
import os

from .auth import role_required
from sqlalchemy.sql import func
from sqlalchemy import desc

student = Blueprint("student", __name__)


@student.route("/dashboard", methods=["GET", "POST"])
@login_required
@role_required("student")
def dashboard():
    search_query = request.args.get("search_query", "").strip()

    # Get quizzes the student has already attempted
    attempted_quiz_ids = (
        db.session.query(QuizResult.quiz_id).filter_by(user_id=current_user.id).all()
    )
    attempted_quiz_ids = [quiz_id[0] for quiz_id in attempted_quiz_ids]

    # Fetch quizzes the student hasn't attempted yet
    query = Quiz.query.filter(Quiz.id.notin_(attempted_quiz_ids))

    # Apply search filter if a search query is provided
    if search_query:
        query = (
            query.join(Chapter)
            .join(Subject)
            .filter(
                db.or_(
                    Quiz.name.ilike(f"%{search_query}%"),
                    Chapter.name.ilike(f"%{search_query}%"),
                    Subject.name.ilike(f"%{search_query}%"),
                )
            )
        )

    # Retrieve the filtered quizzes
    available_quizzes = query.all()

    return render_template(
        "student/student_dashboard.html",
        user=current_user,
        quizzes=available_quizzes,
        search_query=search_query,  # Pass the search query to the template
    )


@student.route("/scores", methods=["GET"])
@login_required
@role_required("student")
def scores():
    search_query = request.args.get("search_query", "").strip()

    # Apply search filter if a search query is provided
    if search_query:
        quiz_results = (
            QuizResult.query.filter_by(user_id=current_user.id)
            .join(Quiz)
            .join(Chapter)
            .join(Subject)
            .filter(
                db.or_(
                    Quiz.name.ilike(f"%{search_query}%"),
                    Chapter.name.ilike(f"%{search_query}%"),
                    Subject.name.ilike(f"%{search_query}%"),
                )
            )
            .all()
        )
    else:
        # Fetch all quiz results for the logged-in student
        quiz_results = QuizResult.query.filter_by(user_id=current_user.id).all()

    # Render the scores page
    return render_template(
        "student/scores.html",
        user=current_user,
        quiz_results=quiz_results,
        search_query=search_query,
    )


@student.route("/summary", methods=["GET", "POST"])
@login_required
@role_required("student")
def summary():
    user = current_user

    total_quizzes_given = QuizResult.query.filter_by(user_id=user.id).count()

    avg_score_by_subject = (
        db.session.query(Subject.name, func.avg(QuizResult.score))
        .join(Chapter, Chapter.subject_id == Subject.id)
        .join(Quiz, Quiz.chapter_id == Chapter.id)
        .join(QuizResult, QuizResult.quiz_id == Quiz.id)
        .filter(QuizResult.user_id == user.id)
        .group_by(Subject.name)
        .all()
    )

    avg_score_by_subject_labels = [subject[0] for subject in avg_score_by_subject]
    avg_score_by_subject_values = [subject[1] for subject in avg_score_by_subject]

    quizzes_by_subject = (
        db.session.query(Subject.name, func.count(QuizResult.id))
        .join(Chapter, Chapter.subject_id == Subject.id)
        .join(Quiz, Quiz.chapter_id == Chapter.id)
        .join(QuizResult, QuizResult.quiz_id == Quiz.id)
        .filter(QuizResult.user_id == user.id)
        .group_by(Subject.name)
        .all()
    )

    quizzes_by_subject_labels = [subject[0] for subject in quizzes_by_subject]
    quizzes_by_subject_values = [subject[1] for subject in quizzes_by_subject]

    return render_template(
        "student/summary.html",
        user=user,
        scores=scores,
        total_quizzes_given=total_quizzes_given,
        quizzes_by_subject_labels=quizzes_by_subject_labels,
        quizzes_by_subject_values=quizzes_by_subject_values,
        avg_score_by_subject_labels=avg_score_by_subject_labels,
        avg_score_by_subject_values=avg_score_by_subject_values,
    )


@student.route("/view_quiz/<int:quiz_id>", methods=["GET"])
@login_required
@role_required("student")
def view_quiz(quiz_id):
    # Fetch the quiz by ID or return a 404 if not found
    quiz = Quiz.query.get_or_404(quiz_id)

    # Render the quiz details page
    return render_template("student/view_quiz.html", user=current_user, quiz=quiz)


@student.route("/take_quiz/<int:quiz_id>", methods=["GET", "POST"])
@login_required
@role_required("student")
def take_quiz(quiz_id):
    # Fetch the quiz by ID or return a 404 if not found
    quiz = Quiz.query.get_or_404(quiz_id)

    if request.method == "POST":
        # Process quiz submission
        selected_options = request.form.getlist("option")
        score = 0

        # Calculate the score based on selected answers
        for question in quiz.questions:
            selected_option_id = request.form.get(f"question_{question.id}")
            if selected_option_id:
                selected_option = Option.query.get(int(selected_option_id))
                if selected_option and selected_option.is_correct:
                    score += 1

        # Store quiz result
        total_questions = len(quiz.questions)
        quiz_result = QuizResult(
            quiz_id=quiz.id,
            user_id=current_user.id,
            score=score,
            total=total_questions,
        )
        db.session.add(quiz_result)
        db.session.commit()

        flash(f"You scored {score}/{total_questions}!", category="success")
        return redirect(url_for("student.scores"))

    # Render the quiz taking page
    return render_template("student/take_quiz.html", user=current_user, quiz=quiz)
