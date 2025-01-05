from flask import Flask, send_from_directory
from werkzeug.utils import safe_join
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_migrate import Migrate
import os
from os import path
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from flask_caching import Cache
from dotenv import load_dotenv

load_dotenv()


db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
mail = Mail()
cache = Cache()

DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config.from_object("backend.config.Config")
    app.config["ALLOWED_EXTENSIONS"] = set(
        os.getenv("ALLOWED_EXTENSIONS", "").split(",")
    )
    cache = Cache(
        config={
            "CACHE_TYPE": os.getenv("CACHE_TYPE", "redis"),
            "CACHE_REDIS_URL": os.getenv("CACHE_REDIS_URL"),
            "CACHE_DEFAULT_TIMEOUT": os.getenv("CACHE_DEFAULT_TIMEOUT"),
        }
    )
    app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER")
    api = Api(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": ["http://localhost:5173"],  # Your Vue.js development server
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "expose_headers": ["Content-Range", "X-Content-Range"],
                "supports_credentials": True,
            }
        },
    )

    @app.after_request
    def apply_cors(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = (
            "GET, POST, PUT, DELETE, OPTIONS"
        )
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response

    from .api.auth import Login, Register
    from .api.student import (
        Student,
        StudentActivity,
        StudentStatistics,
        StudentSubjectPerformance,
    )
    from .api.admin import Admin
    from .api.subject import SubjectApi
    from .api.chapter import ChapterApi
    from .api.quiz import QuizApi
    from .api.question import QuestionApi
    from .api.options import OptionApi
    from .api.options import OptionsBulkApi
    from .api.serve_file import FileApi

    api.add_resource(Student, "/api/students", "/api/student/<int:student_id>")
    api.add_resource(StudentStatistics, "/api/student/statistics")
    api.add_resource(StudentActivity, "/api/student/<int:student_id>/activity")
    api.add_resource(
        StudentSubjectPerformance, "/api/student/<int:student_id>/subjects"
    )
    api.add_resource(Login, "/api/login")
    api.add_resource(Register, "/api/register")
    api.add_resource(Admin, "/api/admin")
    api.add_resource(SubjectApi, "/api/subject", "/api/subject/<int:subject_id>")
    api.add_resource(ChapterApi, "/api/chapter", "/api/chapter/<int:chapter_id>")
    api.add_resource(QuizApi, "/api/quizzes", "/api/quizzes/<int:quiz_id>")
    api.add_resource(
        QuestionApi,
        "/api/quizzes/<int:quiz_id>/questions",
        "/api/quizzes/<int:quiz_id>/questions/<int:question_id>",
    )
    api.add_resource(
        OptionApi,
        "/api/questions/<int:question_id>/options",
        "/api/options/<int:option_id>",
    )
    api.add_resource(OptionsBulkApi, "/api/questions/<int:question_id>/options/bulk")
    api.add_resource(FileApi, "/api/uploads/subjects/<path:filename>")

    with app.app_context():
        db.create_all()
    return app


def create_database(app):
    if not path.exists("server/" + DB_NAME):
        db.create_all(app=app)
        print("Created Database!")
