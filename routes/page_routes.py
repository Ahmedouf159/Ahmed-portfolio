from flask import Blueprint, render_template

page_bp = Blueprint("pages", __name__)

@page_bp.get("/")
def home():
    return render_template("index.html")

@page_bp.get("/about")
def about():
    return render_template("about.html")

@page_bp.get("/services")
def services():
    return render_template("services.html")

@page_bp.get("/projects")
def projects():
    return render_template("projects.html")
