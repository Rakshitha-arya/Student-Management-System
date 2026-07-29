from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User Login View."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        login_identity = request.form.get('identity')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user, err_msg = AuthService.authenticate_user(login_identity, password)
        if user:
            login_user(user, remember=remember)
            flash(f"Welcome back, {user.username}! Logged in as {user.role}.", "success")
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.index'))
        else:
            flash(err_msg, "danger")

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User Registration View."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role', 'Staff')

        if password != confirm_password:
            flash("Passwords do not match. Please re-enter.", "danger")
            return render_template('register.html', username=username, email=email, role=role)

        user, errors = AuthService.register_user(username, email, password, role)
        if user:
            flash("Registration successful! You can now log in with your credentials.", "success")
            return redirect(url_for('auth.login'))
        else:
            for err in errors:
                flash(err, "danger")

    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Logs out current user and clears session."""
    logout_user()
    flash("You have been successfully logged out.", "info")
    return redirect(url_for('auth.login'))
