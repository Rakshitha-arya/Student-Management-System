from extensions import db
from models.user import User
from utils.validators import Validator

class AuthService:
    """Service layer handling user authentication and registration operations."""

    @staticmethod
    def register_user(username: str, email: str, password: str, role: str = 'Staff') -> tuple[User | None, list[str]]:
        """Registers a new user after validation."""
        errors = []
        
        username = Validator.sanitize(username)
        email = Validator.sanitize(email).lower()

        if not username or len(username) < 3:
            errors.append("Username must be at least 3 characters long.")
        elif User.query.filter_by(username=username).first():
            errors.append(f"Username '{username}' is already taken.")

        valid_email, err_email = Validator.validate_email(email, model_type='user')
        if not valid_email:
            errors.append(err_email)

        if not password or len(password) < 6:
            errors.append("Password must be at least 6 characters long.")

        if role not in ['Admin', 'Staff']:
            role = 'Staff'

        if errors:
            return None, errors

        # Instantiate OOP model
        user = User(
            username=username,
            email=email,
            role=role
        )
        user.set_password(password)

        try:
            db.session.add(user)
            db.session.commit()
            return user, []
        except Exception as e:
            db.session.rollback()
            return None, [f"Database error during user registration: {str(e)}"]

    @staticmethod
    def authenticate_user(login_identity: str, password: str) -> tuple[User | None, str]:
        """Authenticates user by username or email and verifies password."""
        identity = Validator.sanitize(login_identity)
        if not identity or not password:
            return None, "Username/Email and Password are required."

        # Search by username or email
        user = User.query.filter(
            (User.username == identity) | (User.email == identity.lower())
        ).first()

        if not user or not user.check_password(password):
            return None, "Invalid credentials. Please check your username/email and password."

        return user, ""

    @staticmethod
    def get_all_users():
        """Returns list of all registered portal users."""
        return User.query.order_by(User.created_at.desc()).all()
