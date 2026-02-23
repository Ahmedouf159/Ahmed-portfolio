from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils.decorators import guest_only
from services.auth_service import signup_user, login_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["GET", "POST"])
@guest_only
def signup():
    if request.method == "POST":
        ok, msg = signup_user(
            request.form.get("username"),
            request.form.get("email"),
            request.form.get("password"),
            request.form.get("confirm_password")
        )
        flash(msg, "success" if ok else "error")
        return redirect(url_for("auth.login" if ok else "auth.signup"))
    return render_template("signup.html")

@auth_bp.route("/login", methods=["GET", "POST"])
@guest_only
def login():
    if request.method == "POST":
        remember = request.form.get("remember_me") == "on"
        user, msg = login_user(
            request.form.get("login_id"),
            request.form.get("password")
        )
        if not user:
            flash(msg, "error")
            return redirect(url_for("auth.login"))

        session.clear()
        session["user_id"] = user["id"]
        session.permanent = remember  # remember-me

        flash(msg, "success")
        return redirect(url_for("user.dashboard"))

    return render_template("login.html")

@auth_bp.get("/logout")
def logout():
    session.clear()
    flash("Logged out.", "success")
    return redirect(url_for("pages.home"))
