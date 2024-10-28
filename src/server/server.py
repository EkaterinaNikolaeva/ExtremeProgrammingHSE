from flask import Flask, render_template, redirect, url_for, request, flash
from flask import jsonify
from flask_login import LoginManager, login_user, login_required, current_user

from src.db.models import User, Homework

app = Flask(__name__)
storage = {}

app = Flask(__name__)
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
    homeworks = Homework.query.filter_by(student_id=current_user.user_id).all()
    return render_template('submitted_works.html', homeworks=homeworks)


def run_server(config, port=9001):
    app.run(port=port, debug=False)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        password = request.form.get('password')

        # TODO check with DB
        if user_id == "admin" and password == "password":
            user = User(user_id)
            login_user(user)
            flash("Успешный вход!", "success")
            next_page = request.args.get('next')
            return redirect(next_page or url_for('protected'))
        else:
            flash("Неверный логин или пароль.", "danger")
    return render_template('login.html')


@app.route('/protected')
@login_required
def protected():
    return f'Привет, {current_user.id}!'

@app.route('/')
def home():
    return redirect(url_for('login'))

