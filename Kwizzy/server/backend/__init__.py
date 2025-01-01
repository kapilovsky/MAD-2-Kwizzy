from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate
from .models import User
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

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    api = Api(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)

    CORS(app, resources={r"/*": {"origins": app.config.get('FRONTEND_URL'), "supports_credentials": True}})

    from .auth import auth
    from .student import student
    from .admin import admin

    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(student, url_prefix="/student")
    app.register_blueprint(admin, url_prefix="/admin")

    with app.app_context():
        db.create_all()  # Create all tables

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists("server/" + DB_NAME):
        db.create_all(app=app)
        print("Created Database!")
