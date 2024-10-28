from flask import Flask, jsonify, request

app = Flask(__name__)
storage = {}


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


@app.route("/storage", methods=["PUT"])
def add_key_value():
    if "key" not in request.json or "value" not in request.json:
        raise RequestException(401, "key and value is required")
    key = request.json["key"]
    value = request.json["value"]
    storage[key] = value
    return (
        jsonify(
            {
                "message": "Ok",
            }
        ),
        201,
    )


@app.route("/storage", methods=["GET"])
def get_key_value():
    if "key" not in request.args:
        raise RequestException(401, "key is required")
    key = request.args["key"]
    if key not in storage:
        raise RequestException(404, "this key not found!")
    return (
        jsonify(
            {
                "value": storage[key],
            }
        ),
        200,
    )


@app.route("/bad", methods=["POST"])
def bad():
    raise RequestException(403, "this operation is forbidden")


@app.route("/hello")
def hello_world():
    return (
        jsonify(
            {
                "message": "Hello, world!",
            }
        ),
        200,
    )


def run_server(port=9001):
    app.run(port=port, debug=False)
