import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "change-me")
DEBUG = os.getenv("DEBUG", "1") == "1"
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin","django.contrib.auth","django.contrib.contenttypes",
    "django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles",
    "rest_framework","cors headers","app",
]

MIDDLEWARE = ["cors headers.middleware.CorsMiddleware","django.middleware.security.SecurityMiddleware",
              "django.contrib.sessions.middleware.SessionMiddleware","django.middleware.common.CommonMiddleware",
              "django.middleware.csrf.CsrfViewMiddleware","django.contrib.auth.middleware.AuthenticationMiddleware",
              "django.contrib.messages.middleware.MessageMiddleware","django.middleware.clickjacking.XFrameOptionsMiddleware",]

ROOT_URLCONF = "TMS.urls"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQL_DATABASE","TMS_db"),
        "USER": os.getenv("MYSQL_USER","root"),
        "PASSWORD": os.getenv("MYSQL_PASSWORD","password"),
        "HOST": os.getenv("MYSQL_HOST","db"),
        "PORT": os.getenv("MYSQL_PORT","3306"),
    }
}

AUTH_USER_MODEL = "app.User"

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
