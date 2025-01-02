from flask_restful import Resource
from flask import request, jsonify


class Student(Resource):
    def get(self):
        return {"student": "student"}
