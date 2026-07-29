import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

DEPARTMENTS = [
    'Computer Science & Engineering',
    'Information Science & Engineering',
    'Electronics & Communication Engineering',
    'Electrical & Electronics Engineering',
    'Mechanical Engineering',
    'Civil Engineering',
    'Data Science & AI',
    'Artificial Intelligence & Machine Learning'
]

def allowed_file(filename: str) -> bool:
    """Checks if uploaded file has an allowed image extension."""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in current_app.config['ALLOWED_EXTENSIONS']

def save_student_photo(file_storage) -> str:
    """Saves photo securely with a unique UUID filename and returns the filename."""
    if not file_storage or not file_storage.filename:
        return 'default_avatar.png'

    if not allowed_file(file_storage.filename):
        raise ValueError("Invalid image file format. Allowed formats: PNG, JPG, JPEG, GIF, WEBP.")

    filename = secure_filename(file_storage.filename)
    ext = filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    
    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    
    file_path = os.path.join(upload_folder, unique_filename)
    file_storage.save(file_path)
    return unique_filename

def get_department_list() -> list[str]:
    """Returns static list of engineering departments."""
    return DEPARTMENTS
