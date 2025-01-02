from flask_restful import Resource


class Admin(Resource):
    def get(self):
        return {"admin": "admin"}
    