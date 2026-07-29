import unittest
from datetime import date
from app import create_app
from extensions import db
from models.user import User
from models.student import Student
from services.auth_service import AuthService
from services.student_service import StudentService
from utils.validators import Validator

class TestStudentPortal(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_authentication_and_hashing(self):
        user, errors = AuthService.register_user('testadmin', 'testadmin@college.edu', 'Pass@123', role='Admin')
        self.assertEqual(len(errors), 0)
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password('Pass@123'))
        self.assertFalse(user.check_password('WrongPass'))
        self.assertTrue(user.is_admin)

        auth_user, err = AuthService.authenticate_user('testadmin', 'Pass@123')
        self.assertIsNotNone(auth_user)
        self.assertEqual(auth_user.id, user.id)

    def test_duplicate_usn_and_email_validation(self):
        payload1 = {
            'usn': '1MS21CS099',
            'name': 'Student One',
            'department': 'Computer Science & Engineering',
            'semester': 5,
            'dob': '2003-05-10',
            'gender': 'Male',
            'email': 'student1@college.edu',
            'phone': '9876543210',
            'address': '123 Test Street'
        }
        std1, errs1 = StudentService.create_student(payload1)
        self.assertEqual(len(errs1), 0)

        # Duplicate USN test
        payload2 = payload1.copy()
        payload2['email'] = 'unique2@college.edu'
        std2, errs2 = StudentService.create_student(payload2)
        self.assertIsNone(std2)
        self.assertTrue(any('USN' in e for e in errs2))

        # Duplicate Email test
        payload3 = payload1.copy()
        payload3['usn'] = '1MS21CS100'
        std3, errs3 = StudentService.create_student(payload3)
        self.assertIsNone(std3)
        self.assertTrue(any('Email' in e for e in errs3))

    def test_invalid_input_validation(self):
        # Invalid phone & invalid semester
        payload = {
            'usn': '1MS21CS101',
            'name': 'Bad Data',
            'department': 'Mechanical Engineering',
            'semester': 12, # Invalid semester
            'dob': '2003-05-10',
            'gender': 'Male',
            'email': 'baddata@college.edu',
            'phone': '123', # Invalid phone
            'address': 'Short'
        }
        std, errs = StudentService.create_student(payload)
        self.assertIsNone(std)
        self.assertTrue(len(errs) >= 2)

    def test_student_crud_and_pagination(self):
        payload = {
            'usn': '1MS21IS055',
            'name': 'Sample CRUD Student',
            'department': 'Information Science & Engineering',
            'semester': 3,
            'dob': '2004-01-15',
            'gender': 'Female',
            'email': 'crud.student@college.edu',
            'phone': '9988776655',
            'address': '789 Silicon Valley Road'
        }
        std, errs = StudentService.create_student(payload)
        self.assertEqual(len(errs), 0)

        # Read
        fetched = StudentService.get_student_by_id(std.id)
        self.assertEqual(fetched.name, 'Sample CRUD Student')

        # Update
        payload['name'] = 'Updated CRUD Student'
        updated, update_errs = StudentService.update_student(std.id, payload)
        self.assertEqual(len(update_errs), 0)
        self.assertEqual(updated.name, 'Updated CRUD Student')

        # Delete
        success, msg = StudentService.delete_student(std.id)
        self.assertTrue(success)
        self.assertIsNone(StudentService.get_student_by_id(std.id))

if __name__ == '__main__':
    unittest.main()
