from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from services.student_service import StudentService

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def root():
    """Redirects root URL to dashboard or login."""
    return redirect(url_for('dashboard.index'))

@dashboard_bp.route('/dashboard')
@login_required
def index():
    """Renders main overview dashboard with aggregate statistics."""
    stats = StudentService.get_dashboard_stats()
    return render_template('dashboard.html', stats=stats)
