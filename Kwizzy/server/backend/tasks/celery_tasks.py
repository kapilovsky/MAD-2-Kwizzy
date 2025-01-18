from __future__ import print_function
from .. import celery
from ..models import User, QuizResult, Quiz
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import logging
from jinja2 import Environment, FileSystemLoader
from ..utils import IndianTimeZone, EmailRateLimiter


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = Environment(loader=FileSystemLoader(template_dir))

logger = logging.getLogger(__name__)

load_dotenv()
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key["api-key"] = os.getenv("BREVO_API_KEY")

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
    sib_api_v3_sdk.ApiClient(configuration)
)


class EmailService:
    def __init__(self):
        self.rate_limiter = EmailRateLimiter()

    @staticmethod
    def send_email(to_email, to_name, subject, template_name, template_data):
        try:
            # Create rate limiter instance
            rate_limiter = EmailRateLimiter()

            # Check if we can send more emails
            if not rate_limiter.can_send_email():
                logger.warning(
                    f"Daily email limit reached. Cannot send email to {to_email}"
                )
                return False

            # Render HTML template
            template = jinja_env.get_template(f"{template_name}")

            # Render HTML content
            html_content = template.render(**template_data)

            sender = {"name": "Kwizzy", "email": os.getenv("MAIL_DEFAULT_SENDER")}

            to = [{"email": to_email, "name": to_name}]

            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=to, html_content=html_content, sender=sender, subject=subject
            )
            api_response = api_instance.send_transac_email(send_smtp_email)
            rate_limiter.increment_count()
            logger.info(f"Email sent successfully to {to_email}")
            return True

        except ApiException as e:
            logger.error(f"Failed to send email: {e}")
            return False


@celery.task
def send_daily_reminders():
    """Send daily reminder to inactive user"""
    try:
        rate_limiter = EmailRateLimiter()
        remaining_emails = rate_limiter.get_remaining_emails()

        if remaining_emails <= 0:
            logger.warning("Daily email limit reached. Skipping reminder sends.")
            return {
                "status": "warning",
                "message": "Daily email limit reached",
                "details": {"remaining_quota": 0},
            }

        students = User.query.filter_by(role="student").all()
        if not students:
            logger.info("No students found in the database")
            return {"status": "success", "message": "No students to send reminders to"}
        # Get new quizzes
        new_quizzes = Quiz.query.order_by(Quiz.id.desc()).limit(3).all()

        successful_sends = 0
        failed_sends = 0

        for student in students:
            if not rate_limiter.can_send_email():
                skipped_sends += len(students) - (successful_sends + failed_sends)
                logger.warning(
                    f"Daily limit reached. Skipping remaining {skipped_sends} students"
                )
                break
            try:
                template_data = {
                    "student_name": student.name,
                    "new_quizzes": new_quizzes,
                    "dashboard_url": f"{os.getenv('FRONTEND_URL')}/login",
                }

                result = EmailService.send_email(
                    to_email=student.email,
                    to_name=student.name,
                    subject="Your Daily Quiz Practice Reminder",
                    template_name="daily_reminder.html",
                    template_data=template_data,
                )

                if result:
                    successful_sends += 1
                    logger.info(f"Reminder sent successfully to {student.email}")
                else:
                    failed_sends += 1
                    logger.error(f"Failed to send reminder to {student.email}")

            except ApiException as e:
                failed_sends += 1
                logger.error(f"Failed to send reminder to {student.email}: {str(e)}")
                continue

        return {
            "status": "success",
            "message": f"Daily reminders processed. Success: {successful_sends}, Failed: {failed_sends}, Skipped: {skipped_sends}",
            "details": {
                "successful_sends": successful_sends,
                "failed_sends": failed_sends,
                "skipped_sends": skipped_sends,
                "total_students": len(students),
                "remaining_quota": rate_limiter.get_remaining_emails(),
            },
        }

    except Exception as e:
        logger.error(f"Error in send_daily_reminders task: {str(e)}")
        return {
            "status": "error",
            "message": f"Failed to process daily reminders: {str(e)}",
        }

    except Exception as e:
        logger.error(f"Error sending reminder: {e}")
        return {"status": "error", "message": str(e)}


@celery.task
def generate_monthly_activity_report():
    """
    Generate and send monthly activity reports for all students
    Scheduled to run on the first day of each month
    """
    try:
        rate_limiter = EmailRateLimiter()
        remaining_emails = rate_limiter.get_remaining_emails()

        if remaining_emails <= 0:
            logger.warning(
                "Daily email limit reached. Skipping generating monthly reports."
            )
            return {
                "status": "warning",
                "message": "Daily email limit reached",
                "details": {"remaining_quota": 0},
            }

        # Get previous month's date range
        today = datetime.now()
        first_day_current = today.replace(day=1)
        last_day_previous = first_day_current - timedelta(days=1)
        first_day_previous = last_day_previous.replace(day=1)

        logger.info(
            f"Generating monthly reports for period: {first_day_previous.strftime('%B %Y')}"
        )

        # Get all students
        students = User.query.filter_by(role="student").all()

        successful_sends = 0
        failed_sends = 0

        for student in students:
            try:
                if not rate_limiter.can_send_email():
                    skipped_sends += len(students) - (successful_sends + failed_sends)
                    logger.warning(
                        f"Daily limit reached. Skipping remaining {skipped_sends} students"
                    )
                    break
                # Get student's quiz activity for previous month
                monthly_quiz_results = (
                    QuizResult.query.join(Quiz)
                    .filter(
                        QuizResult.user_id == student.id,
                        QuizResult.completed_at >= first_day_previous,
                        QuizResult.completed_at <= last_day_previous,
                    )
                    .all()
                )

                # Calculate statistics
                total_quizzes = len(monthly_quiz_results)
                if total_quizzes == 0:
                    continue  # Skip if no activity

                total_score = sum(
                    (result.marks_scored / result.total_marks) * 100
                    for result in monthly_quiz_results
                )
                average_score = round(total_score / total_quizzes, 2)

                # Get performance by subject
                subject_performance = {}
                for result in monthly_quiz_results:
                    subject_name = result.quiz.chapter.subject.name
                    if subject_name not in subject_performance:
                        subject_performance[subject_name] = {
                            "total_quizzes": 0,
                            "total_score": 0,
                        }
                    subject_performance[subject_name]["total_quizzes"] += 1
                    subject_performance[subject_name]["total_score"] += (
                        result.marks_scored / result.total_marks
                    ) * 100

                # Calculate average score per subject
                for subject in subject_performance.values():
                    subject["average_score"] = round(
                        subject["total_score"] / subject["total_quizzes"], 2
                    )

                # Get best performance
                best_quiz = max(
                    monthly_quiz_results, key=lambda x: (x.marks_scored / x.total_marks)
                )
                best_score = round(
                    (best_quiz.marks_scored / best_quiz.total_marks) * 100, 2
                )

                # Prepare template data
                template_data = {
                    "student_name": student.name,
                    "report_period": first_day_previous.strftime("%B %Y"),
                    "total_quizzes": total_quizzes,
                    "average_score": average_score,
                    "best_score": best_score,
                    "best_quiz_name": best_quiz.quiz.name,
                    "subject_performance": subject_performance,
                    "quiz_history": [
                        {
                            "date": result.completed_at.strftime("%Y-%m-%d"),
                            "quiz_name": result.quiz.name,
                            "score": round(
                                (result.marks_scored / result.total_marks) * 100, 2
                            ),
                        }
                        for result in monthly_quiz_results
                    ],
                    "dashboard_url": f"{os.getenv('FRONTEND_URL')}/student/{student.id}",
                }

                # Send email
                result = EmailService.send_email(
                    to_email=student.email,
                    to_name=student.name,
                    subject=f"Your Monthly Activity Report - {first_day_previous.strftime('%B %Y')}",
                    template_name="monthly_report.html",
                    template_data=template_data,
                )

                if result:
                    successful_sends += 1
                    logger.info(f"Monthly report sent successfully to {student.email}")
                else:
                    failed_sends += 1
                    logger.error(f"Failed to send monthly report to {student.email}")

            except Exception as e:
                failed_sends += 1
                logger.error(f"Error processing report for {student.email}: {str(e)}")
                continue

        return {
            "status": "success",
            "message": f"Monthly reports processed. Success: {successful_sends}, Failed: {failed_sends}",
            "details": {
                "successful_sends": successful_sends,
                "failed_sends": failed_sends,
                "total_students": len(students),
                "period": first_day_previous.strftime("%B %Y"),
                "remaining_quota": rate_limiter.get_remaining_emails(),
                "skipped_sends": skipped_sends,
            },
        }

    except Exception as e:
        logger.error(f"Error in monthly report generation: {str(e)}")
        return {
            "status": "error",
            "message": f"Failed to process monthly reports: {str(e)}",
        }


@celery.task
def send_export_notification(to_email, to_name, subject, download_url):
    """Send notification when export is ready"""
    try:
        rate_limiter = EmailRateLimiter()

        if not rate_limiter.can_send_email():
            logger.warning(
                f"Daily email limit reached. Cannot send export notification to {to_email}"
            )
            return {"status": "error", "message": "Daily email limit reached"}
        template_data = {
            "user_name": to_name,
            "export_type": subject,
            "download_url": download_url,
            "generation_time": IndianTimeZone().strftime("%Y-%m-%d %H:%M"),
            "expiry_note": "This download link will expire in 7 days.",
        }

        result = EmailService.send_email(
            to_email=to_email,
            to_name=to_name,
            subject=f"Your {subject} is Ready",
            template_name="export_ready.html",
            template_data=template_data,
        )

        if result:
            logger.info(f"Export notification sent successfully to {to_email}")
            return {"status": "success", "message": "Notification sent"}
        else:
            logger.error(f"Failed to send export notification to {to_email}")
            return {"status": "error", "message": "Failed to send notification"}

    except Exception as e:
        logger.error(f"Error sending export notification: {str(e)}")
        return {"status": "error", "message": str(e)}


@celery.task
def test_email_template(to_email, to_name):
    """Test email template rendering and sending"""
    try:
        template_data = {
            "user_name": to_name,
            "new_quizzes": [
                {"name": "Test Quiz 1", "description": "Test Description 1"},
                {"name": "Test Quiz 2", "description": "Test Description 2"},
            ],
            "dashboard_url": "http://localhost:5173/login",
        }

        EmailService.send_email(
            to_email=to_email,
            to_name=to_name,
            subject="Test Email Template",
            template_name="daily_reminder.html",
            template_data=template_data,
        )

        return {"status": "success", "message": "Test email sent"}

    except Exception as e:
        logger.error(f"Error sending test email: {e}")
        return {"status": "error", "message": str(e)}
