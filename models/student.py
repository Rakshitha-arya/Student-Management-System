from datetime import datetime, timezone, date
from extensions import db

class Student(db.Model):
    """Student Model for Academic Records."""
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    usn = db.Column(db.String(20), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    department = db.Column(db.String(100), nullable=False, index=True)
    semester = db.Column(db.Integer, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    photo_filename = db.Column(db.String(255), nullable=True, default='default_avatar.png')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    @property
    def formatted_dob(self) -> str:
        """Returns DOB in YYYY-MM-DD format."""
        if isinstance(self.dob, (date, datetime)):
            return self.dob.strftime('%Y-%m-%d')
        return str(self.dob)

    def to_dict(self) -> dict:
        """Serializes Student model into dictionary for API/JSON export."""
        return {
            'id': self.id,
            'usn': self.usn,
            'name': self.name,
            'department': self.department,
            'semester': self.semester,
            'dob': self.formatted_dob,
            'gender': self.gender,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'photo_filename': self.photo_filename,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self) -> str:
        return f"<Student usn='{self.usn}' name='{self.name}' dept='{self.department}'>"
