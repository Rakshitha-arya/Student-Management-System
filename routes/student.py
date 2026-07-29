from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required
from services.student_service import StudentService
from utils.helpers import get_department_list, save_student_photo
from utils.decorators import admin_required, staff_required

student_bp = Blueprint('student', __name__, url_prefix='/students')

@student_bp.route('/')
@login_required
@staff_required
def list_students():
    """Lists students with search filters, department filter, semester filter, and pagination."""
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '').strip()
    department = request.args.get('department', '').strip()
    semester = request.args.get('semester', '').strip()

    per_page = current_app.config.get('STUDENTS_PER_PAGE', 8)
    pagination = StudentService.get_paginated_students(
        page=page,
        per_page=per_page,
        search_query=search_query,
        department=department,
        semester=semester
    )

    departments = get_department_list()
    return render_template(
        'students.html',
        pagination=pagination,
        students=pagination.items,
        departments=departments,
        search_query=search_query,
        selected_dept=department,
        selected_sem=semester
    )

@student_bp.route('/add', methods=['GET', 'POST'])
@login_required
@staff_required
def add_student():
    """Renders and processes New Student Registration Form."""
    departments = get_department_list()
    
    if request.method == 'POST':
        data = {
            'usn': request.form.get('usn'),
            'name': request.form.get('name'),
            'department': request.form.get('department'),
            'semester': request.form.get('semester'),
            'dob': request.form.get('dob'),
            'gender': request.form.get('gender'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'address': request.form.get('address')
        }

        # Process uploaded photo if attached
        photo_filename = 'default_avatar.png'
        if 'photo' in request.files and request.files['photo'].filename != '':
            try:
                photo_filename = save_student_photo(request.files['photo'])
            except ValueError as val_err:
                flash(str(val_err), "danger")
                return render_template('add_student.html', departments=departments, form_data=data)

        student, errors = StudentService.create_student(data, photo_filename=photo_filename)
        if student:
            flash(f"Student '{student.name}' ({student.usn}) registered successfully!", "success")
            return redirect(url_for('student.list_students'))
        else:
            for err in errors:
                flash(err, "danger")
            return render_template('add_student.html', departments=departments, form_data=data)

    return render_template('add_student.html', departments=departments, form_data={})

@student_bp.route('/<int:student_id>/edit', methods=['GET', 'POST'])
@login_required
@staff_required
def edit_student(student_id: int):
    """Renders and processes Student Update Form."""
    student = StudentService.get_student_by_id(student_id)
    if not student:
        flash("Student record not found.", "danger")
        return redirect(url_for('student.list_students'))

    departments = get_department_list()

    if request.method == 'POST':
        data = {
            'usn': request.form.get('usn'),
            'name': request.form.get('name'),
            'department': request.form.get('department'),
            'semester': request.form.get('semester'),
            'dob': request.form.get('dob'),
            'gender': request.form.get('gender'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'address': request.form.get('address')
        }

        photo_filename = None
        if 'photo' in request.files and request.files['photo'].filename != '':
            try:
                photo_filename = save_student_photo(request.files['photo'])
            except ValueError as val_err:
                flash(str(val_err), "danger")
                return render_template('edit_student.html', student=student, departments=departments)

        updated_student, errors = StudentService.update_student(student_id, data, photo_filename=photo_filename)
        if updated_student:
            flash(f"Student record for '{updated_student.name}' updated successfully!", "success")
            return redirect(url_for('student.list_students'))
        else:
            for err in errors:
                flash(err, "danger")

    return render_template('edit_student.html', student=student, departments=departments)

@student_bp.route('/<int:student_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_student(student_id: int):
    """Deletes student record (Admin Role Protected)."""
    success, message = StudentService.delete_student(student_id)
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    return redirect(url_for('student.list_students'))
