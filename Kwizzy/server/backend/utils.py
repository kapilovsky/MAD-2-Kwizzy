from functools import wraps
from flask_jwt_extended import get_jwt
from flask import current_app as app
import pytz
from datetime import datetime
import redis
import os
import logging

logger = logging.getLogger(__name__)


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


class EmailRateLimiter:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            db=int(os.getenv("REDIS_DB", 0)),
        )
        self.daily_limit = 300  # Brevo free tier limit

    def can_send_email(self):
        """Check if we can send more emails today"""
        today = datetime.now().strftime("%Y-%m-%d")
        key = f"email_count:{today}"

        # Get current count
        count = int(self.redis_client.get(key) or 0)

        if count >= self.daily_limit:
            logger.warning(f"Daily email limit reached: {count}/{self.daily_limit}")
            return False

        return True

    def increment_count(self):
        """Increment the email count for today"""
        today = datetime.now().strftime("%Y-%m-%d")
        key = f"email_count:{today}"

        # Increment counter
        new_count = self.redis_client.incr(key)

        # Set expiry if not already set
        if new_count == 1:
            # Set to expire at midnight
            seconds_until_midnight = (
                (24 - datetime.now().hour) * 3600
                - datetime.now().minute * 60
                - datetime.now().second
            )
            self.redis_client.expire(key, seconds_until_midnight)

        return new_count

    def get_remaining_emails(self):
        """Get remaining email quota for today"""
        today = datetime.now().strftime("%Y-%m-%d")
        key = f"email_count:{today}"

        count = int(self.redis_client.get(key) or 0)
        remaining = self.daily_limit - count

        return max(0, remaining)
