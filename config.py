import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "capstone-student-mgmt-super-secret-key-2026"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload folder
    if os.environ.get("VERCEL"):
        UPLOAD_FOLDER = "/tmp/uploads"
    else:
        UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg",
        "gif",
        "webp"
    }

    STUDENTS_PER_PAGE = 8

    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True


class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DEV_DATABASE_URL")
        or "sqlite:///" + os.path.join(BASE_DIR, "database", "student_portal.db")
    )


class TestingConfig(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or "sqlite:///" + os.path.join(BASE_DIR, "database", "student_portal_prod.db")
    )


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
