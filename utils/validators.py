import re
from datetime import datetime
from models.student import Student
from models.user import User

class Validator:
    """Centralized Input Validator Class for Data Integrity."""

    USN_REGEX = r'^[1-4][A-Z]{2}\d{2}[A-Z]{2,3}\d{3}$'  # Standard Indian USN pattern e.g., 1MS21CS045
    PHONE_REGEX = r'^[6-9]\d{9}$'                      # 10-digit Indian mobile number standard
    EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    @staticmethod
    def sanitize(value: str) -> str:
        """Strips leading/trailing whitespace and normalizes string."""
        return value.strip() if isinstance(value, str) else ''

    @classmethod
    def validate_usn(cls, usn: str, current_student_id: int = None) -> tuple[bool, str]:
        """Validates USN format and uniqueness."""
        usn = cls.sanitize(usn).upper()
        if not usn:
            return False, "USN / Roll Number is required."
        if len(usn) < 5 or len(usn) > 20:
            return False, "USN must be between 5 and 20 characters long."
        
        # Check uniqueness in database
        existing = Student.query.filter_by(usn=usn).first()
        if existing and (current_student_id is None or existing.id != current_student_id):
            return False, f"USN '{usn}' is already registered to another student."
        
        return True, ""

    @classmethod
    def validate_email(cls, email: str, model_type='student', record_id: int = None) -> tuple[bool, str]:
        """Validates email format and uniqueness across User or Student models."""
        email = cls.sanitize(email).lower()
        if not email:
            return False, "Email address is required."
        if not re.match(cls.EMAIL_REGEX, email):
            return False, "Invalid email address format."

        if model_type == 'student':
            existing = Student.query.filter_by(email=email).first()
            if existing and (record_id is None or existing.id != record_id):
                return False, f"Email '{email}' is already registered to another student."
        elif model_type == 'user':
            existing = User.query.filter_by(email=email).first()
            if existing and (record_id is None or existing.id != record_id):
                return False, f"Email '{email}' is already registered to another user."

        return True, ""

    @classmethod
    def validate_phone(cls, phone: str) -> tuple[bool, str]:
        """Validates 10-digit phone number format."""
        phone = cls.sanitize(phone)
        if not phone:
            return False, "Phone number is required."
        clean_phone = re.sub(r'[\s\-\(\)\+]', '', phone)
        if not (clean_phone.isdigit() and len(clean_phone) == 10):
            return False, "Phone number must be exactly 10 digits."
        return True, ""

    @classmethod
    def validate_semester(cls, semester) -> tuple[bool, str]:
        """Validates semester range (1 to 8)."""
        try:
            sem = int(semester)
            if sem < 1 or sem > 8:
                return False, "Semester must be between 1 and 8."
            return True, ""
        except (ValueError, TypeError):
            return False, "Semester must be a valid integer number."

    @classmethod
    def validate_dob(cls, dob_str: str) -> tuple[bool, str]:
        """Validates Date of Birth string format (YYYY-MM-DD) and reasonable age limit."""
        if not dob_str:
            return False, "Date of Birth is required."
        try:
            dob_date = datetime.strptime(dob_str, '%Y-%m-%d').date()
            today = datetime.today().date()
            age = (today - dob_date).days // 365
            if age < 15 or age > 70:
                return False, "Student age must be between 15 and 70 years."
            return True, ""
        except ValueError:
            return False, "Date of Birth must be in YYYY-MM-DD format."

    @classmethod
    def validate_student_payload(cls, data: dict, current_student_id: int = None) -> list[str]:
        """Runs comprehensive validation on all student fields and returns list of error messages."""
        errors = []

        # Name validation
        name = cls.sanitize(data.get('name'))
        if not name or len(name) < 2:
            errors.append("Full Name is required and must be at least 2 characters.")

        # USN validation
        valid_usn, err_usn = cls.validate_usn(data.get('usn'), current_student_id)
        if not valid_usn:
            errors.append(err_usn)

        # Department validation
        dept = cls.sanitize(data.get('department'))
        if not dept:
            errors.append("Department is required.")

        # Semester validation
        valid_sem, err_sem = cls.validate_semester(data.get('semester'))
        if not valid_sem:
            errors.append(err_sem)

        # DOB validation
        valid_dob, err_dob = cls.validate_dob(data.get('dob'))
        if not valid_dob:
            errors.append(err_dob)

        # Gender validation
        gender = cls.sanitize(data.get('gender'))
        if gender not in ['Male', 'Female', 'Other']:
            errors.append("Please select a valid gender option.")

        # Email validation
        valid_email, err_email = cls.validate_email(data.get('email'), model_type='student', record_id=current_student_id)
        if not valid_email:
            errors.append(err_email)

        # Phone validation
        valid_phone, err_phone = cls.validate_phone(data.get('phone'))
        if not valid_phone:
            errors.append(err_phone)

        # Address validation
        address = cls.sanitize(data.get('address'))
        if not address or len(address) < 5:
            errors.append("Address is required and must be at least 5 characters.")

        return errors
