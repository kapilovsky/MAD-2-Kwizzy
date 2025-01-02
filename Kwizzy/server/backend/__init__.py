from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_migrate import Migrate
from os import path
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from flask_caching import Cache

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
mail = Mail()
cache = Cache()

DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config.from_object("backend.config.Config")
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

    api.add_resource(Student, "/api/student")
    api.add_resource(Login, "/api/login")
    api.add_resource(Register, "/api/register")
    api.add_resource(Admin, "/api/admin")
    api.add_resource(SubjectApi, "/api/subject")
    api.add_resource(ChapterApi, "/api/chapter")

    with app.app_context():
        db.create_all()
    return app


def create_database(app):
    if not path.exists("server/" + DB_NAME):
        db.create_all(app=app)
        print("Created Database!")
