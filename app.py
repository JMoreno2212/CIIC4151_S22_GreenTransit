from flask import Flask, request, jsonify, url_for
from flask_cors import CORS

from backend.controller.delivery import BaseDelivery
from backend.controller.dispensary import BaseDispensary
from backend.controller.driver import BaseDriver
from backend.controller.item import BaseItem
from backend.controller.license import BaseLicense
from backend.controller.purchase import BasePurchase
from backend.controller.user import BaseUser
from backend.controller.vehicle import BaseVehicle
from backend.model.license import LicenseDAO

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return "<h1>Welcome to the Green Transit App Homepage</h1> <p>This we application was created by the Green " \
           "Transit Team and it serves as its Capstone Project Demonstration </p>"


# --------------------------------------------------------------------------------------
# Registration
# --------------------------------------------------------------------------------------
@app.route('/register', methods=['POST'])
def verifyRegistration():
    if request.method == 'POST':
        if request.json['registration_type'] == "User":
            return BaseUser().createUser(request.json)
        elif request.json['registration_type'] == "Driver":
            return BaseDriver().createDriver(request.json)
        elif request.json['registration_type'] == "Dispensary":
            return BaseDispensary().createDispensary(request.json)
        else:
            return jsonify("No registration type found"), 404
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/login', methods=['POST'])
def verifyLogin():
    if request.method == 'POST':
        if request.json['login_type'] == "User":
            return BaseUser().verifyUserLogin(request.json)
        elif request.json['login_type'] == "Driver":
            return BaseDriver().verifyDriverLogin(request.json)
        elif request.json['registration_type'] == "Dispensary":
            return BaseDispensary().verifyDispensaryLogin(request.json)
        else:
            return jsonify("No login type found"), 404
    else:
        return jsonify("Method Not Allowed"), 405


# --------------------------------------------------------------------------------------
# Delivery
# --------------------------------------------------------------------------------------
@app.route('/Delivery/deliveries/all', methods=['GET'])
def handleDeliveries():
    if request.method == 'GET':
        return BaseDelivery().getAllDeliveries()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Delivery/deliveries/<int:delivery_id>', methods=['GET'])
def handleDeliveryById(delivery_id):
    if request.method == 'GET':
        return BaseDelivery().getDeliveryById(delivery_id)
    else:
        return jsonify("Method Not Allowed"), 405


# --------------------------------------------------------------------------------------
# Dispensary
# --------------------------------------------------------------------------------------
@app.route('/Dispensary/dispensaries/all', methods=['GET'])
def handleDispensaries():
    if request.method == 'GET':
        return BaseDispensary().getAllDispensaries()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Dispensary/dispensaries/active', methods=['GET'])
def handleActiveDispensaries():
    if request.method == 'GET':
        return BaseDispensary().getAllActiveDispensaries()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Dispensary/dispensaries/<int:dispensary_id>', methods=['GET'])
def handleDispensaryById(dispensary_id):
    if request.method == 'GET':
        return BaseDispensary().getDispensaryById(dispensary_id)
    else:
        return jsonify("Method Not Allowed"), 405


# --------------------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------------------
@app.route('/Driver/drivers/all', methods=['GET'])
def handleDrivers():
    if request.method == 'GET':
        return BaseDriver().getAllDrivers()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Driver/drivers/active', methods=['GET'])
def handleActiveDrivers():
    if request.method == 'GET':
        return BaseDriver().getAllActiveDrivers()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Driver/drivers/<int:driver_id>', methods=['GET'])
def handleDriverById(driver_id):
    if request.method == 'GET':
        return BaseDriver().getDriverById(driver_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Driver/drivers/<int:driver_id>/registervehicle', methods=['POST'])
def handleDriverVehicleRegistration(driver_id):
    if request.method == 'POST':
        return BaseVehicle().createVehicle(driver_id, request.json)
    else:
        return jsonify("Method Not Allowed"), 405


# --------------------------------------------------------------------------------------
# Item
# --------------------------------------------------------------------------------------
@app.route('/Item/items/all', methods=['GET'])
def handleItems():
    if request.method == 'GET':
        return BaseItem().getAllItems()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Item/items/active', methods=['GET'])
def handleActiveItems():
    if request.method == 'GET':
        return BaseItem().getAllActiveItems()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Item/items/<int:item_id>', methods=['GET'])
def handleItemById(item_id):
    if request.method == 'GET':
        return BaseItem().getItemById(item_id)
    else:
        return jsonify("Method Not Allowed"), 405


# --------------------------------------------------------------------------------------
# Licenses
# --------------------------------------------------------------------------------------
@app.route('/License/licenses/all', methods=['GET'])
def handleLicenses():
    if request.method == 'GET':
        return BaseLicense().getAllLicenses()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/License/licenses/active', methods=['GET'])
def handleActiveLicenses():
    if request.method == 'GET':
        return BaseLicense().getAllActiveLicenses()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/testing/licenses', methods=['POST'])
def handleCreateLicense():
    return str(LicenseDAO().createLicense("Testing", "license123.pdf", "2030-10-10", "file.pdf"))


@app.route('/License/licenses/<int:license_id>', methods=['GET'])
def handleLicenseById(license_id):
    if request.method == 'GET':
        return BaseLicense().getLicensesById(license_id)
    else:
        return jsonify("Method Not Allowed"), 405


# --------------------------------------------------------------------------------------
# Purchase
# --------------------------------------------------------------------------------------
@app.route('/Purchase/purchases', methods=['GET'])
def handlePurchases():
    if request.method == 'GET':
        return BasePurchase().getAllPurchases()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Purchase/purchases/<int:purchase_id>', methods=['GET'])
def handlePurchasesById(purchase_id):
    if request.method == 'GET':
        return BasePurchase().getPurchaseById(purchase_id)
    else:
        return jsonify("Method Not Allowed"), 405


# --------------------------------------------------------------------------------------
# User
# --------------------------------------------------------------------------------------
@app.route('/User/users/all', methods=['GET'])
def handleUsers():
    if request.method == 'GET':
        return BaseUser().getAllUsers()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/User/users/active', methods=['GET'])
def handleActiveUsers():
    if request.method == 'GET':
        return BaseUser().getAllActiveUsers()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/User/users/<int:user_id>', methods=['GET'])
def handleUsersById(user_id):
    if request.method == 'GET':
        return BaseUser().getUserById(user_id)
    else:
        return jsonify("Method Not Allowed"), 405


# --------------------------------------------------------------------------------------
# Vehicle
# --------------------------------------------------------------------------------------
@app.route('/Vehicle/vehicles/all', methods=['GET'])
def handleVehicles():
    if request.method == 'GET':
        return BaseVehicle().getAllVehicles()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Vehicle/vehicles/active', methods=['GET'])
def handleActiveVehicles():
    if request.method == 'GET':
        return BaseVehicle().getAllActiveVehicles()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Vehicle/vehicles/<int:vehicle_id>', methods=['GET'])
def handleVehicleById(vehicle_id):
    if request.method == 'GET':
        return BaseVehicle().getVehicleById(vehicle_id)
    else:
        return jsonify("Method Not Allowed"), 405


# --------------------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------------------
if __name__ == 'main':
    app.run()
