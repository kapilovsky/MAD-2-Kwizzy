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
from sqlalchemy.orm import aliased
from .auth import role_required
from sqlalchemy.sql import func
from sqlalchemy import desc

admin = Blueprint("admin", __name__)


@admin.route("/dashboard", methods=["GET", "POST"])
@login_required
@role_required("admin")
def dashboard():
    search_query = request.args.get("search_query", "").strip()
    if search_query:
        # Filter subjects based on search query (case-insensitive)
        subjects = Subject.query.filter(Subject.name.ilike(f"%{search_query}%")).all()
    else:
        # Return all subjects if no search query is provided
        subjects = Subject.query.all()
    return render_template(
        "admin/admin_dashboard.html",
        user=current_user,
        subjects=subjects,
        search_query=search_query,
    )


@admin.route("/add_subject", methods=["GET", "POST"])
@login_required
@role_required("admin")
def add_subject():
    if request.method == "POST":
        subject_name = request.form.get("subject_name")
        description = request.form.get("description")
        if not subject_name or not description:
            flash("Please fill in all fields", category="error")
            return redirect(url_for("admin.add_subject"))
        # Add subject to the database
        subject = Subject(name=subject_name, description=description)
        db.session.add(subject)
        db.session.commit()
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/add_subject.html", user=current_user)


@admin.route("/edit_subject/<int:subject_id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    if request.method == "POST":
        subject.name = request.form.get("subject_name")
        subject.description = request.form.get("description")
        db.session.commit()
        return redirect(url_for("admin.dashboard"))
    return render_template(
        "admin/edit_subject.html", user=current_user, subject=subject
    )


@admin.route("/delete_subject/<int:subject_id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    db.session.delete(subject)
    db.session.commit()
    return redirect(url_for("admin.dashboard"))


@admin.route("view_subject/<int:subject_id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def view_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    search_query = request.args.get("search_query", "").strip()

    if search_query:
        # Filter chapters within the subject based on the search query (case-insensitive)
        chapters = Chapter.query.filter(
            Chapter.subject_id == subject_id, Chapter.name.ilike(f"%{search_query}%")
        ).all()
    else:
        # Get all chapters if no search query is provided
        chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    return render_template(
        "admin/view_subject.html",
        user=current_user,
        subject=subject,
        chapters=chapters,
        search_query=search_query,
    )


@admin.route("/add_chapter/<int:subject_id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def add_chapter(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    if request.method == "POST":
        chapter_name = request.form.get("chapter_name")
        description = request.form.get("description")
        if not chapter_name or not description:
            flash("Please fill in all fields", category="error")
            return redirect(url_for("admin.add_chapter", subject_id=subject_id))
        # Add chapter to the database
        chapter = Chapter(
            name=chapter_name, description=description, subject_id=subject_id
        )
        db.session.add(chapter)
        db.session.commit()
        return redirect(url_for("admin.view_subject", subject_id=subject_id))
    return render_template("admin/add_chapter.html", user=current_user, subject=subject)


@admin.route("/edit_chapter/<int:chapter_id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    if request.method == "POST":
        chapter.name = request.form.get("chapter_name")
        chapter.description = request.form.get("description")
        db.session.commit()
        return redirect(url_for("admin.view_subject", subject_id=chapter.subject_id))
    return render_template(
        "admin/edit_chapter.html", user=current_user, chapter=chapter
    )


@admin.route("/delete_chapter/<int:chapter_id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def delete_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    db.session.delete(chapter)
    db.session.commit()
    return redirect(url_for("admin.view_subject", subject_id=chapter.subject_id))


@admin.route("view_chapter/<int:chapter_id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def view_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    search_query = request.args.get("search_query", "").strip()

    if search_query:
        # Filter quizzes within the chapter based on the search query (case-insensitive)
        quizzes = Quiz.query.filter(
            Quiz.chapter_id == chapter_id, Quiz.name.ilike(f"%{search_query}%")
        ).all()
    else:
        # Get all quizzes if no search query is provided
        quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()

    quizzes_with_questions = [
        {
            "quiz": quiz,
            "questions": Question.query.filter_by(quiz_id=quiz.id).all(),
            "formatted_time_duration": f"{quiz.time_duration // 3600:02d}:{(quiz.time_duration % 3600) // 60:02d}",
        }
        for quiz in quizzes
    ]
    return render_template(
        "admin/view_chapter.html",
        user=current_user,
        chapter=chapter,
        quizzes=quizzes_with_questions,
        search_query=search_query,
    )


@admin.route("/add_quiz/<int:chapter_id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def add_quiz(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    if request.method == "POST":
        quiz_name = request.form.get("quiz_name")
        description = request.form.get("description")
        time_duration = request.form.get("time_duration")
        if not quiz_name or not description:
            flash("Please fill in all fields", category="error")
            return redirect(url_for("admin.add_quiz", chapter_id=chapter_id))
        try:
            hours, minutes = map(int, time_duration.split(":"))
            total_seconds = hours * 3600 + minutes * 60
        except ValueError:
            flash("Invalid timer format. Please use hh:mm.", category="error")
            return redirect(url_for("admin.add_quiz", chapter_id=chapter_id))
        # Add quiz to the database
        quiz = Quiz(
            name=quiz_name,
            description=description,
            time_duration=total_seconds,
            chapter_id=chapter_id,
        )
        db.session.add(quiz)
        db.session.commit()
        return redirect(url_for("admin.view_chapter", chapter_id=chapter_id))
    return render_template("admin/add_quiz.html", user=current_user, chapter=chapter)


@admin.route("/edit_quiz/<int:quiz_id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    time_in_seconds = quiz.time_duration
    hours = time_in_seconds // 3600
    minutes = (time_in_seconds % 3600) // 60
    formatted_time_duration = f"{hours:02d}:{minutes:02d}"
    if request.method == "POST":
        quiz.name = request.form.get("quiz_name")
        quiz.description = request.form.get("description")
        time_duration = request.form.get("time_duration")
        try:
            hours, minutes = map(int, time_duration.split(":"))
            total_seconds = hours * 3600 + minutes * 60
        except ValueError:
            flash("Invalid timer format. Please use hh:mm.", category="error")
            return redirect(url_for("admin.edit_quiz", quiz_id=quiz_id))
        quiz.time_duration = total_seconds
        db.session.commit()
        return redirect(url_for("admin.view_chapter", chapter_id=quiz.chapter_id))
    return render_template(
        "admin/edit_quiz.html",
        user=current_user,
        quiz=quiz,
        formatted_time_duration=formatted_time_duration,
    )


@admin.route("/delete_quiz/<int:quiz_id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    return redirect(url_for("admin.view_chapter", chapter_id=quiz.chapter_id))


# Utility function for validating options
def validate_options(options):
    if len(options) < 2:
        return "A question must have at least two options."
    if not any(option["is_correct"] for option in options):
        return "At least one option must be marked as correct."
    if sum(option["is_correct"] for option in options) > 1:
        return "Only one option can be marked as correct."
    return None


@admin.route("/add_question/<int:quiz_id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def add_question(quiz_id):

    quiz = Quiz.query.get_or_404(quiz_id)

    if request.method == "POST":
        question_text = request.form.get("question_text")

        # Collect options from the form
        options = []
        print(request.form.keys())
        for key in request.form.keys():
            if key.startswith("option_"):
                index = key.split("_")[1]
                options.append(
                    {
                        "text": request.form[key],
                        "is_correct": request.form.get(f"is_correct_{index}") == "on",
                    }
                )

        # Validate inputs
        error = validate_options(options)
        if error:
            flash(error, "error")
            return redirect(url_for("admin.add_question", quiz_id=quiz_id))

        # Save question and options in the database
        question = Question(text=question_text, quiz_id=quiz_id)
        question.options = [
            Option(text=opt["text"], is_correct=opt["is_correct"]) for opt in options
        ]
        try:
            db.session.add(question)
            db.session.commit()
            flash("Question added successfully", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "error")

        return redirect(
            url_for("admin.view_chapter", quiz_id=quiz_id, chapter_id=quiz.chapter_id)
        )

    return render_template("admin/add_question.html", quiz=quiz)


@admin.route("/edit_question/<int:question_id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_question(question_id):
    question = Question.query.get_or_404(question_id)
    options = question.options
    chapter_id = question.quiz.chapter_id

    if request.method == "POST":
        question.text = request.form.get("question_text")

        # Collect options from the form
        new_options = []
        print(request.form.keys())
        for key in request.form.keys():
            if key.startswith("option_"):
                index = key.split("_")[1]
                new_options.append(
                    {
                        "text": request.form[key],
                        "is_correct": request.form.get(f"is_correct_{index}") == "on",
                    }
                )

        # Validate inputs
        error = validate_options(new_options)
        if error:
            flash(error, "error")
            return redirect(url_for("admin.edit_question", question_id=question_id))

        # Update options
        try:
            # Clear existing options
            db.session.query(Option).filter_by(question_id=question.id).delete()

            # Add new options
            for opt in new_options:
                new_option = Option(
                    text=opt["text"],
                    is_correct=opt["is_correct"],
                    question_id=question.id,
                )
                db.session.add(new_option)

            db.session.commit()
            flash("Question updated successfully", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "error")

        return redirect(url_for("admin.view_chapter", chapter_id=chapter_id))

    return render_template("admin/edit_question.html", question=question)


@admin.route("/delete_question/<int:question_id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    chapter = question.quiz.chapter_id
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for("admin.view_chapter", chapter_id=chapter))


@admin.route("/view_question/<int:question_id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def view_question(question_id):
    question = Question.query.get_or_404(question_id)
    options = question.options
    correct_option = next(opt for opt in options if opt.is_correct)
    return render_template(
        "admin/view_question.html",
        user=current_user,
        question=question,
        options=options,
        correct_option=correct_option,
    )


@admin.route("/summary", methods=["GET", "POST"])
@login_required
@role_required("admin")
def summary():
    subject_count = db.session.query(func.count(Subject.id)).scalar()
    chapter_count = db.session.query(func.count(Chapter.id)).scalar()
    quiz_count = db.session.query(func.count(Quiz.id)).scalar()
    question_count = db.session.query(func.count(Question.id)).scalar()
    # student count where role==student
    student_count = (
        db.session.query(func.count(User.id)).filter(User.role == "student").scalar()
    )

    quizzes_per_subject = (
        db.session.query(Subject.name, func.count(Quiz.id))
        .select_from(Subject)
        .join(Chapter)
        .join(Quiz)
        .group_by(Subject.name)
        .all()
    )

    top_students = (
        db.session.query(User.first_name, func.avg(QuizResult.score))
        .join(QuizResult)
        .group_by(User.id)
        .order_by(func.avg(QuizResult.score).desc())
        .limit(5)
        .all()
    )
    top_students_names = [value[0] for value in top_students]

    average_scores_by_subject = (
        db.session.query(Subject.name, func.avg(QuizResult.score))
        .join(Chapter)
        .join(Quiz)
        .join(QuizResult)
        .group_by(Subject.name)
        .all()
    )

    average_scores_by_subject_labels = [value[0] for value in average_scores_by_subject]
    average_scores_by_subject_values = [value[1] for value in average_scores_by_subject]

    quizzes_per_subject_labels = [value[0] for value in quizzes_per_subject]
    quizzes_per_subject_values = [value[1] for value in quizzes_per_subject]

    return render_template(
        "admin/summary.html",
        user=current_user,
        subject_count=subject_count,
        chapter_count=chapter_count,
        quiz_count=quiz_count,
        question_count=question_count,
        student_count=student_count,
        top_students_names=top_students_names,
        quizzes_per_subject_labels=quizzes_per_subject_labels,
        quizzes_per_subject_values=quizzes_per_subject_values,
        average_scores_by_subject_labels=average_scores_by_subject_labels,
        average_scores_by_subject_values=average_scores_by_subject_values,
    )


@admin.route("/students", methods=["GET", "POST"])
@login_required
@role_required("admin")
def students():
    search_query = request.args.get("search_query", "").strip()

    # Alias for the QuizResult model
    QuizResultAlias = aliased(QuizResult)

    if search_query:
        # Filter students based on search query and their role
        students = (
            db.session.query(
                User, func.count(QuizResultAlias.id).label("test_count")  # Count tests
            )
            .outerjoin(
                QuizResultAlias, QuizResultAlias.user_id == User.id
            )  # Join on QuizResult
            .filter(
                (
                    User.first_name.ilike(f"%{search_query}%")
                    | User.last_name.ilike(f"%{search_query}%")
                )
                & (User.role == "student")
            )
            .group_by(User.id)  # Group by User to count their tests
            .all()
        )
    else:
        # Return all students if no search query is provided
        students = (
            db.session.query(
                User, func.count(QuizResultAlias.id).label("test_count")  # Count tests
            )
            .outerjoin(
                QuizResultAlias, QuizResultAlias.user_id == User.id
            )  # Join on QuizResult
            .filter(User.role == "student")
            .group_by(User.id)  # Group by User to count their tests
            .all()
        )

    students_count = len(students)

    return render_template(
        "admin/students.html",
        user=current_user,
        students=students,  # Students is now a list of tuples (User, test_count)
        search_query=search_query,
        students_count=students_count,
    )
