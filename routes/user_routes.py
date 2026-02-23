from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils.decorators import login_required
from models.user_model import find_user_by_id
from services.user_service import change_username, change_password

user_bp = Blueprint("user", __name__)

@user_bp.get("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@user_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user = find_user_by_id(session["user_id"])
    if not user:
        session.clear()
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        ok1, msg1 = change_username(session["user_id"], request.form.get("username"))
        if msg1:
            flash(msg1, "success" if ok1 else "error")
            if not ok1:
                return redirect(url_for("user.profile"))

        ok2, msg2 = change_password(
            session["user_id"],
            request.form.get("new_password"),
            request.form.get("confirm_new_password"),
        )
        if msg2:
            flash(msg2, "success" if ok2 else "error")
            if not ok2:
                return redirect(url_for("user.profile"))

        return redirect(url_for("user.profile"))

    return render_template("profile.html", user=user)
