from sqlalchemy import (
    Text,
    DateTime,
    func,
    Date,
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from . import db
from .utils import IndianTimeZone, convert_to_ist, format_ist_datetime
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    dob = Column(Date, nullable=False)
    qualification = Column(String(50), nullable=False)
    role = Column(String(10), nullable=False, default="student")
    profile_pic = Column(String(255), nullable=True)
    password = Column(String(30), nullable=False)

    quiz_results = relationship(
        "QuizResult", back_populates="user", cascade="all, delete-orphan"
    )


class Subject(db.Model):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(120), nullable=False)
    subject_image = Column(String(255), nullable=True)

    def to_dict(self):
        quiz_count = sum(len(chapter.quizzes) for chapter in self.chapters)
        # Counting the number of distinct students who have attempted quizzes
        # We join QuizResults with Quizzes, which are linked to Chapters
        student_attempted_count = (
            db.session.query(func.count(func.distinct(QuizResult.user_id)))
            .join(Quiz, Quiz.id == QuizResult.quiz_id)
            .join(Chapter, Chapter.id == Quiz.chapter_id)
            .filter(Chapter.subject_id == self.id)
            .scalar()
        )
        chapter_count = len(self.chapters)
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "subject_image": self.subject_image,
            "quiz_count": quiz_count,
            "students": student_attempted_count,
            "chapters": chapter_count,
        }

    chapters = relationship(
        "Chapter", back_populates="subject", cascade="all, delete-orphan"
    )


class Chapter(db.Model):
    __tablename__ = "chapters"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    subject_id = Column(
        Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False
    )
    description = Column(String(120), nullable=False)

    def to_dict(self):
        quizzes = len(self.quizzes)
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "subject_id": self.subject_id,
            "total_quizzes": quizzes,
        }

    quizzes = relationship(
        "Quiz", back_populates="chapter", cascade="all, delete-orphan"
    )
    subject = relationship("Subject", back_populates="chapters")


class Quiz(db.Model):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(120), nullable=False)
    price = Column(Integer, nullable=False, default=0)
    chapter_id = Column(
        Integer, ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False
    )
    time_duration = Column(Integer, nullable=False, default=0)
    deadline = Column(DateTime, nullable=True)
    one_attempt_only = Column(Boolean, default=True)

    questions = relationship(
        "Question", back_populates="quiz", cascade="all, delete-orphan"
    )
    quiz_results = relationship(
        "QuizResult", back_populates="quiz", cascade="all, delete-orphan"
    )
    chapter = relationship("Chapter", back_populates="quizzes")
    payments = relationship(
        "PaymentHistory", backref="quiz", cascade="all, delete-orphan"
    )

    def has_user_paid(self, user_id):
        return (
            PaymentHistory.query.filter_by(
                user_id=user_id, quiz_id=self.id, status="completed"
            ).first()
            is not None
        )

    def is_available(self):
        """Check if quiz is available based on deadline"""
        if not self.deadline:
            return True
        return datetime.now() < self.deadline

    def has_attempted(self, user_id):
        """Check if user has already attempted this quiz"""
        return (
            QuizResult.query.filter_by(user_id=user_id, quiz_id=self.id).first()
            is not None
        )

    def get_status_message(self):
        """Get appropriate message based on quiz availability"""
        if not self.deadline:
            return "Available"
        if self.is_available():
            return f"Available until {self.deadline.strftime('%Y-%m-%d %H:%M')} IST"
        return f"Deadline passed on {self.deadline.strftime('%Y-%m-%d %H:%M')} IST"

    @staticmethod
    def parse_deadline(deadline_str):
        """Convert string deadline to datetime object"""
        if not deadline_str:
            return None
        try:
            return datetime.fromisoformat(deadline_str.replace("Z", "+00:00"))
        except ValueError:
            # For simpler format without timezone
            return datetime.strptime(deadline_str, "%d-%m-%YT%H:%M")


class Question(db.Model):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(
        Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False
    )
    title = Column(String(100), nullable=True)
    text = Column(String(255), nullable=False)

    options = relationship(
        "Option", back_populates="question", cascade="all, delete-orphan"
    )
    quiz = relationship("Quiz", back_populates="questions")


class Option(db.Model):
    __tablename__ = "options"
    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(
        Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False
    )
    text = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)

    question = relationship("Question", back_populates="options")


# ||----------------------User Answer Model----------------------||#
class UserAnswer(db.Model):
    __tablename__ = "user_answers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    result_id = Column(
        Integer, ForeignKey("quiz_results.id", ondelete="CASCADE"), nullable=False
    )
    question_id = Column(
        Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False
    )
    selected_option = Column(
        Integer, ForeignKey("options.id", ondelete="SET NULL"), nullable=True
    )
    is_correct = Column(Boolean, default=False)

    quiz_result = relationship("QuizResult", back_populates="user_answers")
    question = relationship("Question", backref="user_answers")
    selected_option_rel = relationship("Option", foreign_keys=[selected_option])

    def to_dict(self):
        try:
            # Get Question text
            question_text = None
            if self.question:
                question_text = self.question.text

            # Get selected option text
            selected_option_text = None
            if self.selected_option:
                selected_option = Option.query.get(self.selected_option)
                if selected_option:
                    selected_option_text = selected_option.text

            # Get correct option text
            correct_option = Option.query.filter_by(
                question_id=self.question_id, is_correct=True
            ).first()
            correct_option_text = (
                correct_option.text if correct_option else "No correct option found"
            )

            return {
                "id": self.id,
                "result_id": self.result_id,
                "question_text": (
                    self.question.text if self.question else "Error loading question"
                ),
                "selected_option": self.selected_option,
                "selected_option_text": selected_option_text or "No answer selected",
                "correct_option_text": correct_option_text,
                "is_correct": self.is_correct,
            }
        except Exception as e:
            print(f"Error in UserAnswer.to_dict(): {str(e)}")
            return {
                "id": self.id,
                "result_id": self.result_id,
                "question_id": self.question_id,
                "selected_option": self.selected_option,
                "selected_option_text": "Error loading answer",
                "correct_option_text": "Error loading correct answer",
                "is_correct": self.is_correct,
            }


# ||----------------------Quiz Result Model----------------------||#
class QuizResult(db.Model):
    __tablename__ = "quiz_results"
    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(
        Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    marks_scored = Column(Integer, nullable=True)
    total_marks = Column(Integer, nullable=True)
    completed_at = Column(DateTime, default=IndianTimeZone())

    user = relationship("User", back_populates="quiz_results")
    quiz = relationship("Quiz", back_populates="quiz_results")
    user_answers = relationship(
        "UserAnswer", back_populates="quiz_result", cascade="all, delete", lazy="joined"
    )

    def to_dict(self):
        try:
            return {
                "id": self.id,
                "quiz_id": self.quiz_id,
                "user_id": self.user_id,
                "marks_scored": self.marks_scored,
                "total_marks": self.total_marks,
                "completed_at_formatted": format_ist_datetime(self.completed_at),
                "user_answers": [answer.to_dict() for answer in self.user_answers],
                "quiz_name": self.quiz.name if self.quiz else None,
                "quiz_description": self.quiz.description if self.quiz else None,
            }
        except Exception as e:
            print(f"Error in QuizResult.to_dict(): {str(e)}")
            return {
                "id": self.id,
                "quiz_id": self.quiz_id,
                "user_id": self.user_id,
                "marks_scored": self.marks_scored,
                "total_marks": self.total_marks,
                "completed_at_formatted": format_ist_datetime(self.completed_at),
                "user_answers": [],
                "quiz_name": "Error loading quiz name",
                "quiz_description": "Error loading quiz description",
            }


class PaymentHistory(db.Model):
    __tablename__ = "payment_history"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    transaction_id = Column(String(100), nullable=False)
    amount = Column(Integer, nullable=False)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=IndianTimeZone())

    def to_dict(self):
        quiz_details = Quiz.query.filter_by(id=self.quiz_id).first()
        user_details = User.query.filter_by(id=self.user_id).first()
        return {
            "id": self.id,
            "user": user_details.name,
            "quiz": quiz_details.name,
            "transaction_id": self.transaction_id,
            "amount": self.amount,
            "status": self.status,
            "created_at": format_ist_datetime(self.created_at),
        }
