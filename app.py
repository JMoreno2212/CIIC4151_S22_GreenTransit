from flask import Flask, request, jsonify
from flask_cors import CORS

from backend.controller.dispensary import BaseDispensary
from backend.controller.driver import BaseDriver
from backend.controller.item import BaseItem
from backend.controller.user import BaseUser
from backend.controller.vehicle import BaseVehicle

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
# Dispensary
# --------------------------------------------------------------------------------------
@app.route('/Dispensary/dispensaries', methods=['GET'])
def handleDispensary():
    if request.method == 'GET':
        return BaseDispensary().getAllDispensaries()
    else:
        return jsonify("Method Not Allowed"), 405


# --------------------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------------------
@app.route('/Driver/drivers', methods=['GET'])
def handleUDriver():
    if request.method == 'GET':
        return BaseDriver().getAllDrivers()
    else:
        return jsonify("Method Not Allowed"), 405


# --------------------------------------------------------------------------------------
# Item
# --------------------------------------------------------------------------------------
@app.route('/Item/items', methods=['GET'])
def handleItem():
    if request.method == 'GET':
        return BaseItem().getAllItems()
    else:
        return jsonify("Method Not Allowed"), 405


# --------------------------------------------------------------------------------------
# Vehicle
# --------------------------------------------------------------------------------------
@app.route('/Vehicle/vehicles', methods=['GET'])
def handleVehicles():
    if request.method == 'GET':
        return BaseVehicle().getAllVehicles()
    else:
        return jsonify("Method Not Allowed"), 405


# --------------------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------------------
if __name__ == 'main':
    app.run()
