import sqlalchemy
from .connection import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = "Users"
    user_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    role = sqlalchemy.Column(sqlalchemy.String, nullable=True)

class Student(SqlAlchemyBase):
    __tablename__ = "Students"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(User.user_id), autoincrement=True)
    group = sqlalchemy.Column(sqlalchemy.String, nullable=False)

class Teacher(SqlAlchemyBase):
    __tablename__ = "Teachers"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(User.user_id), autoincrement=True)
    subject = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    group = sqlalchemy.Column(sqlalchemy.String, nullable=False)
