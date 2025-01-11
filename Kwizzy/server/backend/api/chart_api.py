# api/chart_api.py
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from ..utils import role_required
from ..models import User, QuizResult, Quiz, Chapter, Subject
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from .. import db, cache


class ChartDataApi(Resource):
    @jwt_required()
    @role_required("admin")
    # @cache.memoize(timeout=300)
    def get(self, chart_type=None):
        try:
            if chart_type == "performance":
                return self.get_performance_data()
            elif chart_type == "qualifications":
                return self.get_qualification_data()
            elif chart_type == "activity":
                return self.get_activity_data()
            elif chart_type == "subjects":
                return self.get_subject_data()
            else:
                return self.get_all_chart_data()
        except Exception as e:
            return {"error": str(e)}, 500

    def get_performance_data(self):
        """Get performance distribution data"""
        try:
            performance_ranges = {
                "excellent (90-100)": (90, 100),
                "good (70-89)": (70, 89),
                "average (50-69)": (50, 69),
                "below_average (0-49)": (0, 49),
            }

            performance_stats = {}
            for range_name, (min_score, max_score) in performance_ranges.items():
                count = (
                    db.session.query(func.count(func.distinct(User.id)))
                    .join(QuizResult)
                    .filter(
                        User.role == "student",
                        (
                            QuizResult.marks_scored * 100 / QuizResult.total_marks
                        ).between(min_score, max_score),
                    )
                    .scalar()
                )
                performance_stats[range_name] = count

            return {
                "labels": list(performance_ranges.keys()),
                "data": list(performance_stats.values()),
            }
        except Exception as e:
            return {"error": str(e)}, 500

    def get_qualification_data(self):
        """Get qualification distribution data"""
        try:
            qualification_stats = (
                db.session.query(User.qualification, func.count(User.id).label("count"))
                .filter(User.role == "student")
                .group_by(User.qualification)
                .all()
            )

            return {
                "labels": [stat[0] for stat in qualification_stats],
                "data": [stat[1] for stat in qualification_stats],
            }
        except Exception as e:
            return {"error": str(e)}, 500

    def get_activity_data(self):
        """Get student activity data"""
        try:
            total_students = User.query.filter_by(role="student").count()

            active_students = (
                User.query.join(QuizResult)
                .filter(
                    User.role == "student",
                    QuizResult.completed_at >= (datetime.now() - timedelta(days=30)),
                )
                .distinct()
                .count()
            )

            return {
                "labels": ["Active", "Inactive"],
                "data": [active_students, total_students - active_students],
            }
        except Exception as e:
            return {"error": str(e)}, 500

    def get_subject_data(self):
        """Get subject-wise performance data"""
        try:
            subject_stats = (
                db.session.query(
                    Subject.name,
                    func.avg(
                        (QuizResult.marks_scored * 100.0) / QuizResult.total_marks
                    ).label("avg_score"),
                    func.count(func.distinct(QuizResult.user_id)).label(
                        "student_count"
                    ),
                )
                .join(Quiz, Quiz.id == QuizResult.quiz_id)
                .join(Chapter, Chapter.id == Quiz.chapter_id)
                .join(Subject, Subject.id == Chapter.subject_id)
                .group_by(Subject.name)
                .all()
            )
            total_subjects = Subject.query.count()
            total_chapters = Chapter.query.count()
            total_quizzes = Quiz.query.count()

            return {
                "labels": [stat[0] for stat in subject_stats],
                "averageScores": [float(stat[1] or 0) for stat in subject_stats],
                "studentCounts": [stat[2] for stat in subject_stats],
                "totalSubjects": total_subjects,
                "totalChapters": total_chapters,
                "totalQuizzes": total_quizzes,
            }
        except Exception as e:
            return {"error": str(e)}, 500

    def get_all_chart_data(self):
        """Get all chart data in one request"""
        try:
            return {
                "performance": self.get_performance_data(),
                "qualifications": self.get_qualification_data(),
                "activity": self.get_activity_data(),
                "subjects": self.get_subject_data(),
            }
        except Exception as e:
            return {"error": str(e)}, 500

