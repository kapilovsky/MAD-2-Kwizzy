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


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    dob = Column(Date, nullable=False)
    qualification = Column(String(50), nullable=False)
    role = Column(String(10), nullable=False, default="student")
    profile_pic = Column(String(255), nullable=True)
    password = Column(String(30), nullable=False)

    quiz_results = relationship(
        "QuizResult", backref="user", cascade="all, delete-orphan"
    )


class Subject(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(255), nullable=False)
    subject_image = Column(String(255), nullable=True)

    chapters = relationship("Chapter", backref="subject", cascade="all, delete-orphan")


class Chapter(db.Model):
    __tablename__ = "chapters"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    subject_id = Column(
        Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False
    )
    description = Column(String(255), nullable=False)

    quizzes = relationship("Quiz", backref="chapter", cascade="all, delete-orphan")
    subject = relationship("Subject", backref="chapters")


class Quiz(db.Model):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)
    chapter_id = Column(
        Integer, ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False
    )
    time_duration = Column(Integer, nullable=False, default=0)  # Timer in seconds

    questions = relationship("Question", backref="quiz", cascade="all, delete-orphan")
    quiz_results = relationship(
        "QuizResult", backref="quiz", cascade="all, delete-orphan"
    )
    chapter = relationship("Chapter", backref="quizzes")


class Question(db.Model):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(
        Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False
    )
    title = Column(String(100), nullable=True)
    text = Column(Text, nullable=False)

    options = relationship("Option", backref="question", cascade="all, delete-orphan")
    quiz = relationship("Quiz", backref="questions")


class Option(db.Model):
    __tablename__ = "options"
    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(
        Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False
    )
    text = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)

    question = relationship("Question", backref="options")


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

    quiz_result = relationship("QuizResult", backref="user_answers")


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
    completed_at = Column(DateTime, default=func.now())

    user = relationship("User", backref="quiz_results")
    quiz = relationship("Quiz", backref="quiz_results")
    user_answers = relationship(
        "UserAnswer", backref="quiz_result", cascade="all, delete"
    )
