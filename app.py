import os
from flask import Flask, render_template
from config import config_by_name
from extensions import db, login_manager
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.student import student_bp


def create_app(config_name=None):
    """Application Factory Pattern for Student Management System."""

    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(
        config_by_name.get(config_name, config_by_name["default"])
    )

    # Initialize Extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(student_bp)

    # Error Handlers
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        db.session.rollback()
        return render_template("errors/500.html"), 500

    # Ensure Upload Directory exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Create database tables only for local development
    if os.environ.get("VERCEL") is None:
        with app.app_context():
            db.create_all()

    return app


# ==========================================================
# Create a top-level Flask app instance for Vercel
# ==========================================================
app = create_app(os.environ.get("FLASK_ENV", "production"))


# ==========================================================
# Run locally
# ==========================================================
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
