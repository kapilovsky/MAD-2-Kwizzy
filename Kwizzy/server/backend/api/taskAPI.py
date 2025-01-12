from ..tasks.celery_tasks import test_email_template
from flask_restful import Resource
from flask import request, jsonify
from ..models import User


class TaskAPI(Resource):
    def get(self, task_type, task_id):
        result = test_email_template.delay("k4p1ll.23@gmail.com", "Kapil")
        return {"result_id": result.id}, 200
