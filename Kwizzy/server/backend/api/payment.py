from flask_restful import Resource
from ..models import PaymentHistory
from flask_jwt_extended import jwt_required
from flask import request, send_file, current_app
from .. import db
import csv
import os
from uuid import uuid4
from datetime import datetime


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


class TransactionHistoryAPI(Resource):
    @jwt_required()
    def get(self, user_id=None):
        try:
            if not user_id:
                payments = PaymentHistory.query.all()
                return {"payments": [payment.to_dict() for payment in payments]}, 200
            payments = PaymentHistory.query.filter_by(user_id=user_id).all()
            return {"payments": [payment.to_dict() for payment in payments]}, 200
        except Exception as e:
            print("Error:", str(e))
            return {"error": str(e)}, 500


class TransactionExportAPI(Resource):
    @jwt_required()
    def get(self, student_id):
        try:
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"transactions_{student_id}_{timestamp}_{uuid4().hex[:8]}.csv"

            # Create filepath
            csv_folder = os.path.join(current_app.config["UPLOAD_FOLDER"], "csv")
            os.makedirs(csv_folder, exist_ok=True)
            filepath = os.path.join(csv_folder, filename)

            # Get transactions
            transactions = PaymentHistory.query.filter_by(user_id=student_id).all()
            # use to_dict() method to get the data in the required format
            transactions = [payment.to_dict() for payment in transactions]
            print(transactions)

            # Write to CSV
            with open(filepath, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    [
                        "S.No",
                        "Transaction ID",
                        "Quiz Name",
                        "Amount in Rs.",
                        "Payment Date",
                    ]
                )

                for index, transaction in enumerate(transactions, 1):
                    writer.writerow(
                        [
                            index,
                            transaction["transaction_id"],
                            transaction["quiz"],
                            transaction["amount"],
                            transaction["created_at"],
                        ]
                    )

            return send_file(
                filepath,
                as_attachment=True,
                download_name=filename,
                mimetype="text/csv",
            )

        except Exception as e:
            print(f"Error exporting transactions: {str(e)}")
            return {"error": str(e)}, 500
