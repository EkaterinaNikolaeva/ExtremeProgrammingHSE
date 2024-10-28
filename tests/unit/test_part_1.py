import unittest
from flask import Flask
from src.db.models import db, User, Homework, Student, Teacher


class HomeworkAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.init_app(self.app)
        db.create_all()

        self.user = User(username='testuser', password='password', role='student')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.role, 'student')

    def test_homework_creation(self):
        homework = Homework(title='Test Homework', subject='Math', file_path='path/to/file', student_id=self.user.id)
        db.session.add(homework)
        db.session.commit()

        retrieved_homework = Homework.query.filter_by(title='Test Homework').first()
        self.assertIsNotNone(retrieved_homework)
        self.assertEqual(retrieved_homework.subject, 'Math')
        self.assertEqual(retrieved_homework.student_id, self.user.id)

    def test_student_creation(self):
        student = Student(user_id=self.user.id, group='A')
        db.session.add(student)
        db.session.commit()

        retrieved_student = Student.query.filter_by(user_id=self.user.id).first()
        self.assertIsNotNone(retrieved_student)
        self.assertEqual(retrieved_student.group, 'A')

    def test_teacher_creation(self):
        teacher_user = User(username='testteacher', password='password', role='teacher')
        db.session.add(teacher_user)
        db.session.commit()

        teacher = Teacher(user_id=teacher_user.id, subject='Math')
        db.session.add(teacher)
        db.session.commit()

        retrieved_teacher = Teacher.query.filter_by(user_id=teacher_user.id).first()
        self.assertIsNotNone(retrieved_teacher)
        self.assertEqual(retrieved_teacher.subject, 'Math')


if __name__ == '__main__':
    unittest.main()
