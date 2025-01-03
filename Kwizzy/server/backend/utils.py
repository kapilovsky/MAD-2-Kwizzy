from flask import jsonify
from functools import wraps
from flask_jwt_extended import get_jwt
from flask import current_app as app


def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()
            print(claims)
            if "role" not in claims or claims["role"] != role:
                return (
                    {"message": "You don't have the required permissions"},
                    403,
                )
            return fn(*args, **kwargs)

        return decorator

    return wrapper


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )
