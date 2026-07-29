import sys
from pathlib import Path
from datetime import date

# Add project root directory to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app import create_app
from extensions import db
from models.user import User
from models.student import Student

def seed_database():
    """Populates database with initial seed users and sample student records."""
    app = create_app('development')
    with app.app_context():
        print("Recreating database tables...")
        db.create_all()

        # Seed Users if not present
        if User.query.count() == 0:
            print("Seeding Portal Users...")
            admin = User(username='admin', email='admin@college.edu', role='Admin')
            admin.set_password('Admin@123')

            staff = User(username='staff', email='staff@college.edu', role='Staff')
            staff.set_password('Staff@123')

            db.session.add_all([admin, staff])
            db.session.commit()
            print("Users seeded: 'admin' (Admin@123) & 'staff' (Staff@123)")

        # Seed Students if not present
        if Student.query.count() == 0:
            print("Seeding Sample Student Records...")
            sample_students = [
                Student(usn='1MS21CS001', name='Aarav Sharma', department='Computer Science & Engineering', semester=6, dob=date(2003, 5, 14), gender='Male', email='aarav.cs@college.edu', phone='9876543210', address='123 M.G. Road, Bengaluru'),
                Student(usn='1MS21CS045', name='Ananya Rao', department='Computer Science & Engineering', semester=6, dob=date(2003, 9, 21), gender='Female', email='ananya.cs@college.edu', phone='9876543211', address='45 Indiranagar 100ft Rd, Bengaluru'),
                Student(usn='1MS22IS012', name='Rohan Verma', department='Information Science & Engineering', semester=4, dob=date(2004, 2, 10), gender='Male', email='rohan.is@college.edu', phone='9876543212', address='88 Koramangala 4th Block, Bengaluru'),
                Student(usn='1MS22EC030', name='Priya Nair', department='Electronics & Communication Engineering', semester=4, dob=date(2004, 11, 5), gender='Female', email='priya.ec@college.edu', phone='9876543213', address='12 HSR Layout Sector 1, Bengaluru'),
                Student(usn='1MS23DS015', name='Vikram Patel', department='Data Science & AI', semester=2, dob=date(2005, 7, 18), gender='Male', email='vikram.ds@college.edu', phone='9876543214', address='90 Jayanagar 4th T Block, Bengaluru'),
                Student(usn='1MS20ME008', name='Karthik Gowda', department='Mechanical Engineering', semester=8, dob=date(2002, 4, 30), gender='Male', email='karthik.me@college.edu', phone='9876543215', address='56 Malleshwaram 15th Cross, Bengaluru'),
                Student(usn='1MS21AI022', name='Sneha Kulkarni', department='Artificial Intelligence & Machine Learning', semester=6, dob=date(2003, 12, 1), gender='Female', email='sneha.ai@college.edu', phone='9876543216', address='34 Whitefield Main Rd, Bengaluru'),
                Student(usn='1MS22EE005', name='Aditya Joshi', department='Electrical & Electronics Engineering', semester=4, dob=date(2004, 8, 14), gender='Male', email='aditya.ee@college.edu', phone='9876543217', address='77 Rajajinagar 1st Block, Bengaluru'),
                Student(usn='1MS23CV019', name='Meera Menon', department='Civil Engineering', semester=2, dob=date(2005, 3, 25), gender='Female', email='meera.cv@college.edu', phone='9876543218', address='22 Hebbal Flyover Junction, Bengaluru'),
                Student(usn='1MS21CS088', name='Devendra Kumar', department='Computer Science & Engineering', semester=6, dob=date(2003, 1, 19), gender='Male', email='dev.cs@college.edu', phone='9876543219', address='61 Electronic City Phase 1, Bengaluru'),
                Student(usn='1MS22IS040', name='Kavya Hegde', department='Information Science & Engineering', semester=4, dob=date(2004, 6, 11), gender='Female', email='kavya.is@college.edu', phone='9876543220', address='15 Banashankari 3rd Stage, Bengaluru'),
                Student(usn='1MS23EC060', name='Siddharth Gupta', department='Electronics & Communication Engineering', semester=2, dob=date(2005, 10, 8), gender='Male', email='sid.ec@college.edu', phone='9876543221', address='40 Yelahanka New Town, Bengaluru')
            ]
            db.session.add_all(sample_students)
            db.session.commit()
            print(f"Successfully seeded {len(sample_students)} student records into database.")

        print("Data seeding completed successfully!")

if __name__ == '__main__':
    seed_database()
