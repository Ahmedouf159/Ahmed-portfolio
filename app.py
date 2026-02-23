from __future__ import annotations

import os
import sqlite3
from datetime import timedelta
from functools import wraps

from flask import (
    Flask, render_template, request, redirect, url_for,
    session, flash, abort
)
from werkzeug.security import generate_password_hash, check_password_hash


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    # IMPORTANT: set a strong secret key (required for sessions)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-this-secret-key")
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=30)

    os.makedirs(app.instance_path, exist_ok=True)
    app.config["DATABASE"] = os.path.join(app.instance_path, "app.db")

    # ---------- DB ----------
    def get_db() -> sqlite3.Connection:
        conn = sqlite3.connect(app.config["DATABASE"])
        conn.row_factory = sqlite3.Row
        return conn

    def init_db() -> None:
        conn = get_db()
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
        conn.close()

    init_db()

    # ---------- helpers ----------
    def login_required(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not session.get("user_id"):
                flash("Please login first.", "warning")
                return redirect(url_for("login"))
            return view(*args, **kwargs)
        return wrapped

    def current_user():
        """Return dict {id, username, email} or None."""
        uid = session.get("user_id")
        if not uid:
            return None
        conn = get_db()
        row = conn.execute("SELECT id, username, email FROM users WHERE id = ?", (uid,)).fetchone()
        conn.close()
        return dict(row) if row else None

    @app.context_processor
    def inject_user():
        user = current_user()
        return {
            "current_user": user,
            "avatar_letter": (user["username"][:1].lower() if user else None)
        }

    # ---------- routes ----------
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/services")
    def services():
        return render_template("services.html")

    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")
            confirm = request.form.get("confirm_password", "")

            if not username or not email or not password:
                flash("Please fill all fields.", "error")
                return render_template("signup.html")

            if len(username) < 3:
                flash("Username must be at least 3 characters.", "error")
                return render_template("signup.html")

            if password != confirm:
                flash("Passwords do not match.", "error")
                return render_template("signup.html")

            if len(password) < 6:
                flash("Password must be at least 6 characters.", "error")
                return render_template("signup.html")

            pw_hash = generate_password_hash(password)

            try:
                conn = get_db()
                conn.execute(
                    "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                    (username, email, pw_hash),
                )
                conn.commit()
                conn.close()
            except sqlite3.IntegrityError:
                flash("Username or email already exists.", "error")
                return render_template("signup.html")

            flash("Account created. Please login.", "success")
            return redirect(url_for("login"))

        return render_template("signup.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            identity = request.form.get("identity", "").strip().lower()  # username OR email
            password = request.form.get("password", "")
            remember = request.form.get("remember") == "on"

            if not identity or not password:
                flash("Please enter username/email and password.", "error")
                return render_template("login.html")

            conn = get_db()
            user = conn.execute(
                "SELECT id, username, email, password_hash FROM users WHERE lower(username)=? OR lower(email)=?",
                (identity, identity),
            ).fetchone()
            conn.close()

            if not user or not check_password_hash(user["password_hash"], password):
                flash("Invalid login details.", "error")
                return render_template("login.html")

            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["email"] = user["email"]

            # Remember me (permanent session)
            session.permanent = remember

            return redirect(url_for("dashboard"))

        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        flash("Logged out successfully.", "success")
        return redirect(url_for("index"))

    @app.route("/dashboard")
    @login_required
    def dashboard():
        # Use session data to show personalized header + letter
        return render_template("dashboard.html")

    @app.route("/profile", methods=["GET", "POST"])
    @login_required
    def profile():
        user = current_user()
        if not user:
            session.clear()
            return redirect(url_for("login"))

        if request.method == "POST":
            new_username = request.form.get("username", "").strip()

            if len(new_username) < 3:
                flash("Username must be at least 3 characters.", "error")
                return redirect(url_for("profile"))

            try:
                conn = get_db()
                conn.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, user["id"]))
                conn.commit()
                conn.close()
            except sqlite3.IntegrityError:
                flash("This username is already used.", "error")
                return redirect(url_for("profile"))

            # Update session
            session["username"] = new_username
            flash("Username updated.", "success")
            return redirect(url_for("profile"))

        return render_template("profile.html")

    @app.route("/settings")
    @login_required
    def settings():
        return render_template("settings.html")

    # Blog intentionally not ready -> show 404 professional
    @app.route("/blog")
    def blog():
        abort(404)

    # ---------- 404 ----------
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    return app


app = create_app()

if __name__ == "__main__":
    # For MOBILE on same Wi-Fi: keep host=0.0.0.0
    # Open on phone: http://YOUR_PC_IP:5000
    app.run(host="0.0.0.0", port=5000, debug=True)