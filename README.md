# Production-Ready Student Management Portal 🎓

A full-stack, enterprise-grade **Student Management Portal** built using Python, Flask, SQLAlchemy, Flask-Login, Bootstrap 5, and SQLite/PostgreSQL. Designed for academic institutions and software engineering capstone demonstrations adhering to **Clean Architecture** principles.

---

## 🌟 Key Features

### 🔐 Authentication & Security
- **Role-Based Access Control (RBAC)**: Distinguishes between **Admin** (full access & record deletion) and **Staff** (read, create, edit access).
- **Password Security**: Hashing with PBKDF2/SHA-256 via Werkzeug Security.
- **Session Management**: Session timeout handling and protected route decorators (`@admin_required`, `@staff_required`).
- **CSRF & SQL Injection Protection**: Parameterized SQLAlchemy queries & session tokens.

### 📊 Overview Dashboard
- Real-time key metrics: **Total Students**, **Total Departments**, **Total Portal Users**, and **User Role Status**.
- **Quick Action Cards** for high-frequency workflows.
- **Recent Registrations** real-time feed.

### 👨‍🎓 Student Management (CRUD & Directory)
- **Comprehensive Fields**: Student ID, USN/Roll Number, Full Name, Department, Semester, Date of Birth, Gender, Email, Phone, Address, and Student Photo.
- **Advanced Directory Filters**: Real-time text search (USN/Name/Email), Department dropdown filter, and Semester range filter.
- **Pagination**: Server-side paginated table rendering (default 8 records per page).
- **Photo Upload**: Secure UUID-based file saving with format validation.

### 🛡️ Input Validation & Custom Exception Handling
- Full backend validation suite (`utils/validators.py`) enforcing:
  - Unique USN validation
  - Unique Email validation
  - Semester range validation (1 – 8)
  - 10-digit Phone number validation
  - Date of Birth age calculation (15 – 70 years)
  - Non-empty field sanitization
- Custom 404 & 500 error pages with automatic database transaction rollback.

---

## 🏗️ Clean Architecture & Project Structure

```
Student-Management-System/
├── app.py                      # Application Factory Pattern
├── config.py                   # Environment Configurations (Dev, Test, Prod)
├── requirements.txt            # Python Dependencies
├── README.md                   # Project Overview & Setup Guide
├── .gitignore                  # Git Ignore Rules
├── extensions.py               # SQLAlchemy & LoginManager instances
├── test_portal.py              # Automated Unit Test Suite
├── models/                     # Data Layer (SQLAlchemy Models)
│   ├── __init__.py
│   ├── user.py                 # User & Role Model
│   └── student.py              # Student Model
├── services/                   # Business Logic Layer
│   ├── auth_service.py         # Authentication & User registration logic
│   └── student_service.py      # Student CRUD & query service
├── routes/                     # Controller Layer (Flask Blueprints)
│   ├── auth.py                 # Login, Register, Logout routes
│   ├── dashboard.py            # Overview dashboard routes
│   └── student.py              # Student management routes
├── utils/                      # Helper & Validation Utilities
│   ├── validators.py           # Input payload validators
│   ├── helpers.py              # File upload & array helpers
│   └── decorators.py           # Role authorization decorators
├── templates/                  # Jinja2 Views
│   ├── base.html               # Responsive Bootstrap layout
│   ├── login.html              # Authentication login view
│   ├── register.html           # User registration view
│   ├── dashboard.html          # Dashboard view
│   ├── students.html           # Student table view
│   ├── add_student.html        # Create student form
│   ├── edit_student.html       # Edit student form
│   └── errors/
│       ├── 404.html            # Custom 404 Page
│       └── 500.html            # Custom 500 Page
├── static/                     # Web Assets
│   ├── css/style.css           # Custom CSS Theme
│   ├── js/main.js              # Auto-dismiss alerts & modals
│   └── uploads/                # Photo uploads storage
├── database/                   # Database Scripts
│   ├── schema.sql              # Raw SQL DDL Schema reference
│   ├── seed.py                 # Data seeding script
│   └── student_portal.db       # SQLite Database
└── reports/                    # Capstone Deliverables
    ├── er_diagram.md           # Mermaid ER Diagram & Database Spec
    ├── project_report.md       # Comprehensive Capstone Project Report
    └── demo_video_script.md    # 3-5 Minute Presentation Demo Script
```

---

## ⚡ Quickstart & Installation

### Prerequisites
- Python 3.10+
- `pip` (Python package manager)

### 1. Clone & Navigate
```bash
git clone https://github.com/your-username/Student-Management-System.git
cd Student-Management-System
```

### 2. Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Seed Database
Run the seed script to initialize the SQLite database tables and insert pre-configured Admin/Staff credentials & sample student records:
```bash
python database/seed.py
```

### 5. Run Application
```bash
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5000`.

---

## 🔑 Default Credentials

| Role | Username | Email | Password | Privileges |
| :--- | :--- | :--- | :--- | :--- |
| **Admin** | `admin` | `admin@college.edu` | `Admin@123` | Full Access + Delete Records |
| **Staff** | `staff` | `staff@college.edu` | `Staff@123` | View, Add, Edit Records |

---

## 🧪 Running Unit Tests
```bash
python test_portal.py
```

---

## 📜 License & Acknowledgments
Developed as an Internship Capstone Project following Python Flask & Clean Software Architecture guidelines.
