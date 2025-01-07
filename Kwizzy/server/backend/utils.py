from flask import jsonify
from functools import wraps
from flask_jwt_extended import get_jwt
from flask import current_app as app
import pytz
from datetime import datetime


def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()
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


def IndianTimeZone():
    IST = pytz.timezone("Asia/Kolkata")
    return datetime.now(IST)


def convert_to_ist(utc_dt):
    """Converts UTC datetime to IST"""
    if not utc_dt:
        return None

    # If datetime is naive (no timezone info), assume it's UTC
    if utc_dt.tzinfo is None:
        utc_dt = pytz.utc.localize(utc_dt)

    IST = pytz.timezone("Asia/Kolkata")
    ist_dt = utc_dt.astimezone(IST)
    return ist_dt


# Format datetime to string in IST
def format_ist_datetime(dt):
    """Formats datetime to IST string"""
    if not dt:
        return None

    ist_dt = convert_to_ist(dt)
    return ist_dt.strftime(
        "%d-%m-%Y %I:%M:%S %p IST"
    )  # Example: "07-01-2025 10:07:18 PM IST"
