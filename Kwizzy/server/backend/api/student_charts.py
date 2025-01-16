# api/student_chart_api.py
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils import role_required
from ..models import User, QuizResult, Quiz, Chapter, Subject
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from .. import db, cache


class StudentChartsApi(Resource):
    @jwt_required()
    @role_required("student")
    def get(self, chart_type=None):
        try:
            student_id = get_jwt_identity()

            if chart_type == "subject_performance":
                return self.get_subject_performance(student_id)
            elif chart_type == "recent_performance":
                return self.get_recent_performance(student_id)
            elif chart_type == "monthly_progress":
                return self.get_monthly_progress(student_id)
            elif chart_type == "heatmap":
                return self.get_heatmap_data(student_id)
            elif chart_type == "strength_weakness":
                return self.get_strength_weakness(student_id)
            else:
                return self.get_all_student_charts(student_id)
        except Exception as e:
            return {"error": str(e)}, 500

    def get_subject_performance(self, student_id):
        """Get performance breakdown by subject"""
        try:
            subject_stats = (
                db.session.query(
                    Subject.name,
                    func.avg(
                        QuizResult.marks_scored * 100.0 / QuizResult.total_marks
                    ).label("average_score"),
                    func.count(QuizResult.id).label("attempts"),
                )
                .join(Chapter, Subject.id == Chapter.subject_id)
                .join(Quiz, Chapter.id == Quiz.chapter_id)
                .join(QuizResult, Quiz.id == QuizResult.quiz_id)
                .filter(QuizResult.user_id == student_id)
                .group_by(Subject.name)
                .all()
            )

            return {
                "labels": [stat[0] for stat in subject_stats],
                "averageScores": [float(stat[1] or 0) for stat in subject_stats],
                "attempts": [stat[2] for stat in subject_stats],
                "type": "bar",
                "title": "Subject-wise Performance",
            }
        except Exception as e:
            return {"error": str(e)}, 500

    def get_recent_performance(self, student_id):
        """Get last 10 quiz performances"""
        try:
            recent_results = (
                QuizResult.query.join(Quiz)
                .filter(QuizResult.user_id == student_id)
                .order_by(QuizResult.completed_at.desc())
                .limit(10)
                .all()
            )

            return {
                "labels": [result.quiz.name for result in recent_results][::-1],
                "scores": [
                    round((result.marks_scored / result.total_marks) * 100, 2)
                    for result in recent_results
                ][::-1],
                "dates": [
                    result.completed_at.strftime("%Y-%m-%d")
                    for result in recent_results
                ][::-1],
                "type": "line",
                "title": "Recent Quiz Performance",
            }
        except Exception as e:
            return {"error": str(e)}, 500

    # Backend: Enhanced monthly progress data

    def get_monthly_progress(self, student_id):
        """Get monthly progress over the last 6 months"""
        try:
            six_months_ago = datetime.now() - timedelta(days=180)
            monthly_stats = (
                db.session.query(
                    func.strftime("%Y-%m", QuizResult.completed_at).label("month"),
                    func.avg(
                        QuizResult.marks_scored * 100.0 / QuizResult.total_marks
                    ).label("average_score"),
                    func.count(QuizResult.id).label("quizzes_taken"),
                    func.max(
                        QuizResult.marks_scored * 100.0 / QuizResult.total_marks
                    ).label("highest_score"),
                    func.min(
                        QuizResult.marks_scored * 100.0 / QuizResult.total_marks
                    ).label("lowest_score"),
                )
                .filter(
                    QuizResult.user_id == student_id,
                    QuizResult.completed_at >= six_months_ago,
                )
                .group_by("month")
                .order_by("month")
                .all()
            )

            return {
                "labels": [
                    (
                        datetime.strptime(stat[0], "%Y-%m").strftime("%B %Y")
                        if stat[0]
                        else "N/A"
                    )
                    for stat in monthly_stats
                ],
                "averageScores": [float(stat[1] or 0) for stat in monthly_stats],
                "quizCount": [stat[2] for stat in monthly_stats],
                "highestScores": [float(stat[3] or 0) for stat in monthly_stats],
                "lowestScores": [float(stat[4] or 0) for stat in monthly_stats],
                "type": "line",
                "title": "Monthly Performance Overview",
            }
        except Exception as e:
            return {"error": str(e)}, 500

    def get_heatmap_data(self, student_id):
        """Get activity heatmap data for the last year"""
        try:
            one_year_ago = datetime.now() - timedelta(days=365)
            daily_activity = (
                db.session.query(
                    func.date(QuizResult.completed_at).label("date"),
                    func.count(QuizResult.id).label("count"),
                )
                .filter(
                    QuizResult.user_id == student_id,
                    QuizResult.completed_at >= one_year_ago,
                )
                .group_by("date")
                .all()
            )

            heatmap_data = []
            for activity in daily_activity:
                try:
                    heatmap_data.append(
                        {
                            "date": activity[0],
                            "count": int(activity[1]),
                        }
                    )
                except Exception as e:
                    print(f"Error formatting activity: {e}")
                    continue

            return {
                "data": heatmap_data,
                "startDate": one_year_ago.strftime("%Y-%m-%d"),
                "endDate": datetime.now().strftime("%Y-%m-%d"),
            }
        except Exception as e:
            print(f"Error in get_heatmap_data: {e}")  # Debug print
            return {"error": str(e)}, 500

    def get_strength_weakness(self, student_id):
        """Analyze chapter-wise performance to identify strengths and weaknesses"""
        try:
            chapter_stats = (
                db.session.query(
                    Chapter.name,
                    Subject.name.label("subject_name"),
                    func.avg(
                        QuizResult.marks_scored * 100.0 / QuizResult.total_marks
                    ).label("average_score"),
                    func.count(QuizResult.id).label("attempts"),
                )
                .join(Quiz, Chapter.id == Quiz.chapter_id)
                .join(QuizResult, Quiz.id == QuizResult.quiz_id)
                .join(Subject, Chapter.subject_id == Subject.id)
                .filter(QuizResult.user_id == student_id)
                .group_by(Chapter.name, Subject.name)
                .having(func.count(QuizResult.id) >= 1)
                .all()
            )

            # Categorize chapters
            strengths = []
            weaknesses = []
            for stat in chapter_stats:
                chapter_data = {
                    "chapter": stat[0],
                    "subject": stat[1],
                    "score": float(stat[2] or 0),
                    "attempts": stat[3],
                }
                if stat[2] >= 75:
                    strengths.append(chapter_data)
                else:
                    weaknesses.append(chapter_data)

            return {
                "strengths": sorted(strengths, key=lambda x: x["score"], reverse=True),
                "weaknesses": sorted(weaknesses, key=lambda x: x["score"]),
                "type": "analysis",
                "title": "Strength & Weakness Analysis",
            }
        except Exception as e:
            return {"error": str(e)}, 500

    def get_all_student_charts(self, student_id):
        """Get all chart data for student dashboard"""
        try:
            return {
                "subject_performance": self.get_subject_performance(student_id),
                "recent_performance": self.get_recent_performance(student_id),
                "monthly_progress": self.get_monthly_progress(student_id),
                "heatmap": self.get_heatmap_data(student_id),
                "strength_weakness": self.get_strength_weakness(student_id),
            }
        except Exception as e:
            return {"error": str(e)}, 500
