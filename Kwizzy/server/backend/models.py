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
from . import cache


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
    description = Column(String(255), nullable=False)
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
    description = Column(String(255), nullable=False)

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
    description = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False, default=0)
    chapter_id = Column(
        Integer, ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False
    )
    time_duration = Column(Integer, nullable=False, default=0)

    questions = relationship(
        "Question", back_populates="quiz", cascade="all, delete-orphan"
    )
    quiz_results = relationship(
        "QuizResult", back_populates="quiz", cascade="all, delete-orphan"
    )
    chapter = relationship("Chapter", back_populates="quizzes")


class Question(db.Model):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(
        Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False
    )
    title = Column(String(100), nullable=True)
    text = Column(Text, nullable=False)

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

    user = relationship("User", back_populates="quiz_results")
    quiz = relationship("Quiz", back_populates="quiz_results")
    user_answers = relationship(
        "UserAnswer", back_populates="quiz_result", cascade="all, delete"
    )
