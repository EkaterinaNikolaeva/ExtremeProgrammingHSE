from flask import Flask, render_template, redirect, url_for, request, flash
from flask import jsonify
from flask_login import LoginManager, login_user, login_required, current_user
from src.config.config import Config
from src.db.models import User, db, Homework

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
        user = User.query.filter_by(username=login).first()
        if user is None:
            flash("Неверный логин или пароль.", "danger")
            raise RequestException(401, "Incorrect login and password")
        login_user(user)
        flash("Успешный вход!", "success")
        next_page = request.args.get('next')
        return redirect(next_page or url_for('protected'))
    return render_template('login.html')


@app.route('/protected')
@login_required
def protected():
    return f'Привет, {current_user.username}!'

@app.route('/')
def home():
    return redirect(url_for('login'))

