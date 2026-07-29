import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    """Base Configuration Class for Student Management System."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'capstone-student-mgmt-super-secret-key-2026'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File Upload Settings
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max limit
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Pagination
    STUDENTS_PER_PAGE = 8
    
    # Security & Session Settings
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True

class DevelopmentConfig(Config):
    """Development Environment Configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'database', 'student_portal.db')

class TestingConfig(Config):
    """Testing Environment Configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Production Environment Configuration."""
    DEBUG = False
    # Supports SQLite by default or PostgreSQL/MySQL via environment variable
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'database', 'student_portal_prod.db')

config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
