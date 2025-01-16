from ..tasks.celery_tasks import test_email_template, send_daily_reminders, generate_monthly_activity_report
from flask_restful import Resource
from flask import request, jsonify
from ..models import User


class TaskAPI(Resource):
    def get(self):
        result = send_daily_reminders.delay()
        return {"result_id": result.id}, 200
