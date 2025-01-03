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
            r"/*": {
                "origins": "*",
                "supports_credentials": True,
            }
        },
    )

    from .api.auth import Login, Register
    from .api.student import Student
    from .api.admin import Admin
    from .api.subject import SubjectApi
    from .api.chapter import ChapterApi
    from .api.quiz import QuizApi
    from .api.question import QuestionApi
    from .api.options import OptionsApi
    from .api.options import OptionsBulkApi
    from .api.serve_file import FileApi

    api.add_resource(Student, "/api/student")
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
        OptionsApi,
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
