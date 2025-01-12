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
def send_daily_reminder(user_id):
    """Send daily reminder to inactive user"""
    try:
        user = User.query.get(user_id)
        if not user:
            return {"status": "error", "message": "User not found"}

        # Get new quizzes
        last_week = datetime.now() - timedelta(days=7)
        new_quizzes = Quiz.query.filter(Quiz.created_at >= last_week).all()

        template_data = {
            "user_name": user.name,
            "new_quizzes": new_quizzes,
            "dashboard_url": f"{os.getenv('FRONTEND_URL')}/login",
        }

        EmailService.send_email(
            to_email=user.email,
            to_name=user.name,
            subject="Don't forget your daily quiz practice!",
            template_name="daily_reminder.html",
            template_data=template_data,
        )

        return {"status": "success", "message": "Reminder sent"}

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
