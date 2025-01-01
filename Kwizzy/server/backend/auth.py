from flask import Blueprint, request, flash, redirect, url_for, render_template, abort
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
from .models import User
from . import db


auth = Blueprint("auth", __name__)


def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role != role:
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


@auth.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Please fill in all fields", category="error")
            return redirect(url_for("auth.login"))

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                if user.role == "admin":
                    return redirect(url_for("admin.dashboard"))
                else:
                    return redirect(url_for("student.dashboard"))
            flash("Incorrect password, try again.", category="error")
            # Log failed attempt here
        else:
            flash("Email does not exist.", category="error")
            # Log failed attempt here

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        password = request.form.get("password1")
        dob_str = request.form.get("date_of_birth")
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
        qualification = request.form.get("qualification")
        role = request.form.get("role")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists.", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 5 characters.", category="error")
        else:
            new_user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                dob=dob,
                role=role,
                qualification=qualification,
                password=generate_password_hash(password),
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created!", category="success")
            return redirect(url_for("auth.login"))

    return render_template("sign_up.html", user=current_user)
