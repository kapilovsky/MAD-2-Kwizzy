from __future__ import print_function
from .. import celery
from flask import current_app
from ..models import User, QuizResult, Quiz
from flask_mail import Message
from datetime import datetime, timedelta
import flask_excel
from io import StringIO
import csv
from dotenv import load_dotenv
import os
from .. import db, mail
from celery import shared_task

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
