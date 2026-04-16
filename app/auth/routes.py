# app/auth/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.models import User
from app import db, bcrypt

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("Login successful!", "success")

            # Redirect based on role
            if user.role == "admin":
                return redirect(url_for("admin.dashboard"))
            if user.role == "buyer":
                return redirect(url_for("buyer.dashboard"))
            else:
                return redirect(url_for("seller.dashboard"))

        flash("Invalid email or password", "danger")

    return render_template("auth/login.html", body_class='page-login')


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        if User.query.filter_by(email=email).first():
            flash("Email already registered", "warning")
            return redirect(url_for("auth.register"))

        hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

        user = User(email=email, password=hashed_pw, role=role)

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully. Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/auth.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.home"))
