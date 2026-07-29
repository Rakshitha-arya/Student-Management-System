from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db, login_manager

class User(UserMixin, db.Model):
    """User Model representing Portal Users (Admins and Staff)."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='Staff')  # 'Admin' or 'Staff'
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def set_password(self, password: str) -> None:
        """Hashes and sets user password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verifies candidate password against stored hash."""
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self) -> bool:
        """Checks if user holds Admin role."""
        return self.role.lower() == 'admin'

    @property
    def is_staff(self) -> bool:
        """Checks if user holds Staff role."""
        return self.role.lower() in ['staff', 'admin']

    def __repr__(self) -> str:
        return f"<User id={self.id} username='{self.username}' role='{self.role}'>"


@login_manager.user_loader
def load_user(user_id: str):
    """Flask-Login user loader callback."""
    return db.session.get(User, int(user_id))
