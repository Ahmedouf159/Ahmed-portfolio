import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
DB_PATH = os.path.join(INSTANCE_DIR, "app.db")

SECRET_KEY = "CHANGE_THIS_TO_A_LONG_RANDOM_SECRET"
PERMANENT_SESSION_LIFETIME = timedelta(days=14)  # remember-me
