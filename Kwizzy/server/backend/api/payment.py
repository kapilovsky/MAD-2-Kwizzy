from flask_restful import Resource
from ..models import PaymentHistory
from flask_jwt_extended import jwt_required
from flask import request
from .. import db


class PaymentApi(Resource):
    @jwt_required()
    def post(self):
        try:
            data = request.json

            payment = PaymentHistory(
                user_id=data["user_id"],
                quiz_id=data["quiz_id"],
                transaction_id=data["transaction_id"],
                amount=data["amount"],
                status="completed",
            )

            db.session.add(payment)
            db.session.commit()

            return {
                "status": "success",
                "message": "Payment recorded successfully",
            }, 201

        except Exception as e:
            db.session.rollback()
            print("Error:", str(e))
            return {"error": str(e)}, 500

    @jwt_required()
    def get(self, user_id, quiz_id):
        try:
            payment = PaymentHistory.query.filter_by(
                user_id=user_id, quiz_id=quiz_id, status="completed"
            ).first()

            return {"has_paid": payment is not None}, 200
        except Exception as e:
            print("Error:", str(e))
            return {"error": str(e)}, 500
