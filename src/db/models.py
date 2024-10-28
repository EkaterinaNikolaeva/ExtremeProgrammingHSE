from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'student' или 'teacher'

class Homework(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    grade = db.Column(db.Float, nullable=True)
    feedback = db.Column(db.Text, nullable=True)
    student = db.relationship('User', backref='homeworks')
