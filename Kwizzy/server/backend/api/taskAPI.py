from ..tasks.celery_tasks import send_email
from flask_restful import Resource
from flask import request, jsonify
from ..models import User


class TaskAPI(Resource):
    def get(self):
        result = send_email.delay()
        return {"result_id": result.id}, 200
