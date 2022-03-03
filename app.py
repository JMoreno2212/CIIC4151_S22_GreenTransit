from flask import Flask, request, jsonify
from flask_cors import CORS

from backend.controller.user import BaseUser

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return "Welcome to the Green Transit App Homepage"


# --------------------------------------------------------------------------------------
# User
# --------------------------------------------------------------------------------------
@app.route('/User/users', methods=['GET'])
def handleUsers():
    if request.method == 'GET':
        return BaseUser().getAllUsers()
    else:
        return jsonify("Method Not Allowed"), 405


# --------------------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------------------
if __name__ == 'main':
    app.run()
