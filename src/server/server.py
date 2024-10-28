import os

from flask import Flask, render_template, redirect, url_for, request, flash
from flask import jsonify
from flask_login import LoginManager, login_user, login_required, current_user
from werkzeug.utils import secure_filename

from src.config.config import Config
from src.db.models import User, db, Homework, HomeworkForm, Student, Teacher

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
with app.app_context():
    db.create_all()
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class RequestException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


@app.errorhandler(RequestException)
def handle_exception(err):
    response = {
        "message": err.message,
    }
    return jsonify(response), err.status_code


@app.route('/submitted_works')
@login_required
def submitted_works():
    if current_user.role == 'teacher':
        raise RequestException(403, "Submitted works are available only for students")
    homeworks = Homework.query.filter_by(student_id=current_user.id).all()
    return render_template('submitted_works.html', homeworks=homeworks)


def run_server(port=9001):
    app.run(port=port, debug=False)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('user_id')
        password = request.form.get('password')
        user = User.query.filter_by(username=login).first()
        if user is None or user.password != password:
            flash("Неверный логин или пароль.", "danger")
            raise RequestException(401, "Incorrect login and password")
        login_user(user)
        flash("Успешный вход!", "success")
        next_page = request.args.get('next')
        return redirect(next_page or url_for('protected'))
    return render_template('login.html')

@app.route('/unreviewed', methods=['GET'])
def get_unreviewed():
    if current_user.role != 'teacher':
        raise RequestException(403, "Reviewing works are available only for teachers")
    subjects = Teacher.query.filter_by(user_id=current_user.id).all()
    print(subjects)
    all_homeworks = []
    for teacher in subjects:
        homeworks = Homework.query.filter_by(subject=teacher.subject, grade=None).all()
        all_homeworks += homeworks
    return render_template('unreviewed.html', homeworks=all_homeworks)

@app.route('/review', methods=['POST', 'GET'])
def review():
    if current_user.role != 'teacher':
        raise RequestException(403, "Reviewing works are available only for teachers")
    try:
        if request.method == 'GET':
            hw_id = request.args['hw_id']
        else:
            hw_id = request.form['hw_id']
    except:
        raise RequestException(403, "hw id is required")
    hw = Homework.query.filter_by(id=hw_id).first()
    return render_template('review.html', file=hw.file_path)


if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


@app.route('/submit_homework', methods=['GET', 'POST'])
@login_required
def submit_homework():
    if current_user.role != 'student':
        flash('Только студенты могут отправлять задания', 'error')
        return redirect(url_for('protected'))

    form = HomeworkForm()
    student_record = Student.query.filter_by(user_id=current_user.id).first()

    if form.validate_on_submit():
        filename = None
        if form.file.data:
            filename = secure_filename(form.file.data.filename)
            form.file.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        homework = Homework(
            title=form.title.data,
            subject=form.subject.data,
            file_path=filename or '',
            student_id=current_user.id,
            feedback=''
        )
        db.session.add(homework)
        db.session.commit()
        flash('Домашнее задание успешно отправлено', 'success')
        return redirect(url_for('submit_successfully'))

    return render_template('submitHW.html', form=form, student_name=current_user.username,
                           group=student_record.group if student_record else 'Неизвестно')


@app.route('/protected')
@login_required
def protected():
    return f'Привет, {current_user.username}!'


@app.route('/submitted_successfully')
@login_required
def submit_successfully():
    return f'Домашнее задание отправлено успешно!'



@app.route('/')
def home():
    return redirect(url_for('login'))
