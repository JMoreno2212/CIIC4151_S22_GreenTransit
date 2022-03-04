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


@app.route('/Dispensary/dispensaries/<int:dispensary_id>', methods=['GET', 'PUT', 'DELETE'])
def handleDispensaryById(dispensary_id):
    if request.method == 'GET':
        return BaseDispensary().getDispensaryById(dispensary_id)
    # elif request.method == 'PUT':
    #     return BaseDispensary().updateDispensary(dispensary_id, request.json)
    # elif request.method == 'DELETE':
    #     return BaseDispensary().deleteDispensary(dispensary_id)
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


@app.route('/Driver/drivers/<int:driver_id>', methods=['GET', 'PUT', 'DELETE'])
def handleDriverById(driver_id):
    if request.method == 'GET':
        return BaseDriver().getDriverById(driver_id)
    # elif request.method == 'PUT':
    #     return BaseDriver().updateDriver(driver_id, request.json)
    # elif request.method == 'DELETE':
    #     return BaseDriver().deleteDriver(driver_id)
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


@app.route('/Item/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def handleItemById(item_id):
    if request.method == 'GET':
        return BaseItem().getItemById(item_id)
    # elif request.method == 'PUT':
    #     return BaseItem().updateItem(item_id, request.json)
    # elif request.method == 'DELETE':
    #     return BaseItem().deleteItem(item_id)
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


@app.route('/Vehicle/vehicles/<int:vehicle_id>', methods=['GET', 'PUT', 'DELETE'])
def handleVehicleById(vehicle_id):
    if request.method == 'GET':
        return BaseVehicle().getVehicleById(vehicle_id)
    # elif request.method == 'PUT':
    #     return BaseVehicle().updateVehicle(vehicle_id, request.json)
    # elif request.method == 'DELETE':
    #     return BaseVehicle().deleteVehicle(vehicle_id)
    else:
        return jsonify("Method Not Allowed"), 405


# --------------------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------------------
if __name__ == 'main':
    app.run()
