from __future__ import print_function
from .. import celery
from flask import current_app, render_template
from ..models import User, QuizResult, Quiz
from flask_mail import Message
from datetime import datetime, timedelta
import flask_excel
from io import StringIO
import csv
from dotenv import load_dotenv
import os
import logging
from jinja2 import Environment, FileSystemLoader

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
subject = "from the Python SDK!"
sender = {"name": "Sendinblue", "email": "kapilydym23@gmail.com"}
replyTo = {"name": "Sendinblue", "email": "kapilydym23@gmail.com"}
html_content = (
    "<html><body><h1>This is my first transactional email </h1></body></html>"
)
to = [{"email": "k4p1ll.23@gmail.com", "name": "Kapil Yadav"}]
params = {"parameter": "My param value", "subject": "New Subject"}
send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
    to=to,
    # bcc=bcc,
    # cc=cc,
    # reply_to=reply_to,
    # headers=headers,
    html_content=html_content,
    sender=sender,
    subject=subject,
)


@celery.task
def send_email():
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)


class EmailService:
    @staticmethod
    def send_email(to_email, to_name, subject, template_name, template_data):
        try:
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
            logger.info(f"Email sent successfully to {to_email}")
            return True

        except ApiException as e:
            logger.error(f"Failed to send email: {e}")
            return False


@celery.task
def send_daily_reminders():
    """Send daily reminder to inactive user"""
    try:

        students = User.query.filter_by(role="student").all()
        if not students:
            logger.info("No students found in the database")
            return {"status": "success", "message": "No students to send reminders to"}
        # Get new quizzes
        new_quizzes = Quiz.query.order_by(Quiz.id.desc()).limit(3).all()

        successful_sends = 0
        failed_sends = 0

        for student in students:
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
            "message": f"Daily reminders processed. Success: {successful_sends}, Failed: {failed_sends}",
            "details": {
                "successful_sends": successful_sends,
                "failed_sends": failed_sends,
                "total_students": len(students),
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
def send_report_notification(user_id, report_url, report_type="Quiz Performance"):
    """Send notification when report is generated"""
    try:
        user = User.query.get(user_id)
        if not user:
            return {"status": "error", "message": "User not found"}

        template_data = {
            "user_name": user.name,
            "report_type": report_type,
            "report_url": report_url,
            "generation_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "report_period": "Last 30 days",
        }

        EmailService.send_email(
            to_email=user.email,
            to_name=user.name,
            subject=f"Your {report_type} Report is Ready",
            template_name="report_ready.html",
            template_data=template_data,
        )

        return {"status": "success", "message": "Notification sent"}

    except Exception as e:
        logger.error(f"Error sending notification: {e}")
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
