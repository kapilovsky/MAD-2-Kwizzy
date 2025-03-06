from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils import role_required, EmailRateLimiter
from ..models import User, QuizResult, Quiz, Chapter, Subject
from .. import db, celery
from flask import current_app, url_for, request
import csv
import os
from datetime import datetime
import logging
from ..tasks.celery_tasks import send_export_notification

logger = logging.getLogger(__name__)

# Create CSV directory if it doesn't exist
app_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
relative_path = os.getenv("UPLOAD_FOLDER").lstrip("./")
CSV_FOLDER = os.path.join(app_root, relative_path, "csv")
os.makedirs(CSV_FOLDER, exist_ok=True)


class UserQuizExportAPI(Resource):
    def __init__(self):
        self.rate_limiter = EmailRateLimiter()

    @jwt_required()
    def post(self):
        """Trigger quiz export for current user"""
        try:
            user_id = get_jwt_identity()

            # Trigger async task
            task = generate_user_quiz_export.delay(user_id)

            return {
                "message": "Export started successfully",
                "task_id": str(task.id),
            }, 202

        except Exception as e:
            logger.error(f"Error generating user quiz export: {str(e)}")
            return {"error": str(e)}, 500

    @jwt_required()
    def get(self):
        """Get status of export task"""
        task_id = request.args.get("task_id")
        if not task_id:
            return {"error": "Task ID is required"}, 400

        task = celery.AsyncResult(task_id)
        return {
            "task_id": task_id,
            "status": task.status,
            "result": task.result if task.ready() else None,
        }


class AdminQuizExportAPI(Resource):
    @jwt_required()
    @role_required("admin")
    def post(self):
        """Trigger quiz export for all users"""
        try:
            admin_id = get_jwt_identity()

            # Trigger async task
            task = generate_admin_quiz_export.delay(admin_id)

            return {
                "message": "Export started successfully",
                "task_id": str(task.id),
            }, 202

        except Exception as e:
            logger.error(f"Error generating admin quiz export: {str(e)}")
            return {"error": str(e)}, 500

    @jwt_required()
    @role_required("admin")
    def get(self):
        """Get status of export task"""
        task_id = request.args.get("task_id")
        if not task_id:
            return {"error": "Task ID is required"}, 400

        task = celery.AsyncResult(task_id)
        return {
            "task_id": task_id,
            "status": task.status,
            "result": task.result if task.ready() else None,
        }


@celery.task
def generate_user_quiz_export(user_id):
    """Generate CSV export of user's quiz results"""
    try:
        # Check if user exists
        user = User.query.get(user_id)
        if not user:
            return {"status": "error", "message": "User not found"}

        rate_limiter = EmailRateLimiter()
        remaining_emails = rate_limiter.get_remaining_emails()

        if remaining_emails <= 0:
            return {
                "status": "error",
                "message": "Email limit exceeded. Please try again later.",
            }

        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"user_{user_id}_quiz_export_{timestamp}.csv"
        filepath = os.path.join(CSV_FOLDER, filename)

        # Get user's quiz results
        results = (
            QuizResult.query.join(Quiz)
            .join(Chapter)
            .join(Subject)
            .filter(QuizResult.user_id == user_id)
            .order_by(QuizResult.completed_at.desc())
            .all()
        )

        # Write to CSV file
        with open(filepath, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)

            # Write headers
            writer.writerow(
                [
                    "Quiz ID",
                    "Quiz Name",
                    "Chapter",
                    "Subject",
                    "Date Taken",
                    "Score (%)",
                    "Status",
                    "Remarks",
                ]
            )

            # Write data
            for result in results:
                score_percentage = (result.marks_scored / result.total_marks) * 100
                status = "Pass" if score_percentage >= 60 else "Fail"

                writer.writerow(
                    [
                        result.quiz_id,
                        result.quiz.name,
                        result.quiz.chapter.name,
                        result.quiz.chapter.subject.name,
                        result.completed_at.strftime("%Y-%m-%d %H:%M"),
                        f"{score_percentage:.2f}",
                        status,
                        get_remarks(score_percentage),
                    ]
                )

        # Generate download URL
        base_url = os.getenv("BASE_URL", "http://localhost:5000")
        download_url = f"{base_url}/static/uploads/subjects/csv/{filename}"

        # Send email notification
        user = User.query.get(user_id)
        send_export_notification.delay(
            user.email, user.name, "Quiz Export Ready", download_url
        )

        return {"status": "success", "download_url": download_url}

    except Exception as e:
        logger.error(f"Error generating user quiz export: {str(e)}")
        return {"status": "error", "message": str(e)}


@celery.task
def generate_admin_quiz_export(admin_id):
    """Generate CSV export of all users' quiz data"""
    try:
        # Check if admin exists
        admin = User.query.get(admin_id)
        if not admin or admin.role != "admin":
            return {"status": "error", "message": "Admin not found"}

        rate_limiter = EmailRateLimiter()
        remaining_emails = rate_limiter.get_remaining_emails()

        if remaining_emails <= 0:
            return {
                "status": "error",
                "message": "Email limit exceeded. Please try again later.",
            }

        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"admin_export_{timestamp}.csv"
        filepath = os.path.join(CSV_FOLDER, filename)

        # Get all students
        students = User.query.filter_by(role="student").all()

        # Write to CSV file
        with open(filepath, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)

            # Write headers
            writer.writerow(
                [
                    "S.No",
                    "Name",
                    "Email",
                    "Total Quizzes",
                    "Average Score (%)",
                    "Best Score (%)",
                    "Last Quiz Date",
                    "Active Streak (days)",
                    "Subjects Attempted",
                    "Performance Level",
                ]
            )
            index = 1
            # Write data for each student
            for student in students:

                quiz_results = QuizResult.query.filter_by(user_id=student.id).all()

                if quiz_results:
                    total_quizzes = len(quiz_results)
                    avg_score = (
                        sum(
                            (r.marks_scored / r.total_marks) * 100 for r in quiz_results
                        )
                        / total_quizzes
                    )
                    best_score = max(
                        (r.marks_scored / r.total_marks) * 100 for r in quiz_results
                    )
                    last_quiz_date = max(r.completed_at for r in quiz_results)

                    streak = calculate_streak(quiz_results)
                    subjects = len(set(r.quiz.chapter.subject_id for r in quiz_results))
                    performance_level = get_performance_level(avg_score)

                    writer.writerow(
                        [
                            index,
                            student.name,
                            student.email,
                            total_quizzes,
                            f"{avg_score:.2f}",
                            f"{best_score:.2f}",
                            last_quiz_date.strftime("%Y-%m-%d"),
                            streak,
                            subjects,
                            performance_level,
                        ]
                    )
                    index += 1

        # Generate download URL
        base_url = os.getenv("BASE_URL", "http://localhost:5000")
        download_url = f"{base_url}/static/uploads/subjects/csv/{filename}"

        # Send email notification
        admin = User.query.get(admin_id)
        send_export_notification.delay(
            admin.email, admin.name, "Admin Export Ready", download_url
        )

        return {"status": "success", "download_url": download_url}

    except Exception as e:
        logger.error(f"Error generating admin export: {str(e)}")
        return {"status": "error", "message": str(e)}


# Helper functions
def get_remarks(score):
    """Generate remarks based on score"""
    if score >= 90:
        return "Excellent performance!"
    elif score >= 75:
        return "Good job!"
    elif score >= 60:
        return "Satisfactory"
    else:
        return "Needs improvement"


def calculate_streak(quiz_results):
    """Calculate current streak of consecutive days with quizzes"""
    if not quiz_results:
        return 0

    dates = sorted(set(r.completed_at.date() for r in quiz_results), reverse=True)

    streak = 1
    for i in range(len(dates) - 1):
        if (dates[i] - dates[i + 1]).days == 1:
            streak += 1
        else:
            break

    return streak


def get_performance_level(avg_score):
    """Determine performance level based on average score"""
    if avg_score >= 90:
        return "Excellent!"
    elif avg_score >= 75:
        return "Good"
    elif avg_score >= 60:
        return "Average"
    else:
        return "Needs Improvement"


@celery.task
def cleanup_old_exports():
    """Remove CSV files older than 7 days"""
    try:
        current_time = datetime.now()
        for filename in os.listdir(CSV_FOLDER):
            filepath = os.path.join(CSV_FOLDER, filename)
            file_modified = datetime.fromtimestamp(os.path.getmtime(filepath))
            if (current_time - file_modified).days > 7:
                os.remove(filepath)
                logger.info(f"Removed old export: {filename}")
    except Exception as e:
        logger.error(f"Error cleaning up old exports: {str(e)}")
