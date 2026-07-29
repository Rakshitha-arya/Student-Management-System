from datetime import datetime
from sqlalchemy import or_
from extensions import db
from models.student import Student
from models.user import User
from utils.validators import Validator

class StudentService:
    """Service layer handling student database operations, queries, and business logic."""

    @staticmethod
    def get_student_by_id(student_id: int) -> Student | None:
        """Retrieves a single student by primary key ID."""
        return db.session.get(Student, student_id)

    @staticmethod
    def get_student_by_usn(usn: str) -> Student | None:
        """Retrieves a student by USN."""
        return Student.query.filter_by(usn=usn.upper()).first()

    @staticmethod
    def create_student(data: dict, photo_filename: str = 'default_avatar.png') -> tuple[Student | None, list[str]]:
        """Validates payload and inserts a new Student record."""
        errors = Validator.validate_student_payload(data)
        if errors:
            return None, errors

        try:
            dob_date = datetime.strptime(data['dob'], '%Y-%m-%d').date()
            student = Student(
                usn=Validator.sanitize(data['usn']).upper(),
                name=Validator.sanitize(data['name']),
                department=Validator.sanitize(data['department']),
                semester=int(data['semester']),
                dob=dob_date,
                gender=Validator.sanitize(data['gender']),
                email=Validator.sanitize(data['email']).lower(),
                phone=Validator.sanitize(data['phone']),
                address=Validator.sanitize(data['address']),
                photo_filename=photo_filename or 'default_avatar.png'
            )
            db.session.add(student)
            db.session.commit()
            return student, []
        except Exception as e:
            db.session.rollback()
            return None, [f"Database error while saving student: {str(e)}"]

    @staticmethod
    def update_student(student_id: int, data: dict, photo_filename: str = None) -> tuple[Student | None, list[str]]:
        """Updates an existing student record after validation."""
        student = db.session.get(Student, student_id)
        if not student:
            return None, ["Student not found."]

        errors = Validator.validate_student_payload(data, current_student_id=student_id)
        if errors:
            return None, errors

        try:
            student.usn = Validator.sanitize(data['usn']).upper()
            student.name = Validator.sanitize(data['name'])
            student.department = Validator.sanitize(data['department'])
            student.semester = int(data['semester'])
            student.dob = datetime.strptime(data['dob'], '%Y-%m-%d').date()
            student.gender = Validator.sanitize(data['gender'])
            student.email = Validator.sanitize(data['email']).lower()
            student.phone = Validator.sanitize(data['phone'])
            student.address = Validator.sanitize(data['address'])
            
            if photo_filename:
                student.photo_filename = photo_filename

            db.session.commit()
            return student, []
        except Exception as e:
            db.session.rollback()
            return None, [f"Database error while updating student: {str(e)}"]

    @staticmethod
    def delete_student(student_id: int) -> tuple[bool, str]:
        """Deletes a student record from database."""
        student = db.session.get(Student, student_id)
        if not student:
            return False, "Student record not found."
        
        try:
            db.session.delete(student)
            db.session.commit()
            return True, f"Student '{student.name}' ({student.usn}) deleted successfully."
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to delete student: {str(e)}"

    @staticmethod
    def get_paginated_students(page: int = 1, per_page: int = 8, search_query: str = '', department: str = '', semester: str = ''):
        """Fetches filtered, searched, and paginated student list."""
        query = Student.query

        # Search filter (USN or Name)
        if search_query:
            q = f"%{search_query.strip()}%"
            query = query.filter(or_(Student.name.ilike(q), Student.usn.ilike(q), Student.email.ilike(q)))

        # Department filter
        if department:
            query = query.filter(Student.department == department)

        # Semester filter
        if semester and semester.isdigit():
            query = query.filter(Student.semester == int(semester))

        return query.order_by(Student.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def get_dashboard_stats() -> dict:
        """Calculates aggregate dashboard metrics."""
        total_students = Student.query.count()
        total_users = User.query.count()
        
        # Count distinct departments represented
        dept_count = db.session.query(Student.department).distinct().count()
        
        # Get 5 recent student registrations
        recent_students = Student.query.order_by(Student.created_at.desc()).limit(5).all()

        return {
            'total_students': total_students,
            'total_departments': dept_count,
            'total_users': total_users,
            'recent_students': recent_students
        }
