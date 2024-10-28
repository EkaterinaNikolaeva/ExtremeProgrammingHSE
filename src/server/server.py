from flask import Flask, jsonify, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from db.models import User, Student, Teacher

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

    
def run_server(config, port=9001):
    app.run(port=port, debug=False)