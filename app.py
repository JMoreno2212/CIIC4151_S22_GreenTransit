from flask import Flask, request, jsonify
from flask_cors import CORS

from backend.controller.delivery import BaseDelivery
from backend.controller.dispensary import BaseDispensary
from backend.controller.driver import BaseDriver
from backend.controller.item import BaseItem
from backend.controller.license import BaseLicense
from backend.controller.purchase import BasePurchase
from backend.controller.user import BaseUser
from backend.controller.vehicle import BaseVehicle

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
        user = BaseUser().verifyUserLogin(request.json)
        if user is not None:
            return user
        driver = BaseDriver().verifyDriverLogin(request.json)
        if driver is not None:
            return driver
        dispensary = BaseDispensary().verifyDispensaryLogin(request.json)
        if dispensary is not None:
            return dispensary
        return jsonify("Username or Password entered incorrectly"), 404
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/resetpassword', methods=['PUT'])
def resetPassword():
    if request.method == 'PUT':
        user = BaseUser().resetPassword(request.json)
        if user is not None:
            return user
        driver = BaseDriver().resetPassword(request.json)
        if driver is not None:
            return driver
        dispensary = BaseDispensary().resetPassword(request.json)
        if dispensary is not None:
            return dispensary
    else:
        return jsonify("Method Not Allowed"), 405


# --------------------------------------------------------------------------------------
# Delivery
# --------------------------------------------------------------------------------------
@app.route('/Delivery/deliveries/all', methods=['GET', 'POST'])
def handleDeliveries():
    if request.method == 'GET':
        return BaseDelivery().getAllDeliveriesBasicInfo()
    elif request.method == 'POST':
        return BaseDelivery().createDelivery(request.json)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Delivery/deliveries/full-information', methods=['GET'])
def handleDeliveriesFullInfo():
    if request.method == 'GET':
        return BaseDelivery().getAllDeliveriesFullInfo()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Delivery/deliveries/no-driver', methods=['GET'])
def handleDeliveriesWithoutDriver():
    if request.method == 'GET':
        return BaseDelivery().getAllDeliveriesWithoutDriver()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Delivery/deliveries/<int:delivery_id>', methods=['GET', 'PUT'])
def handleDeliveryById(delivery_id):
    if request.method == 'GET':
        return BaseDelivery().getDeliveryByIdBasicInfo(delivery_id)
    elif request.method == 'PUT':
        return BaseDelivery().updateDeliveryInformation(delivery_id, request.json)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Delivery/deliveries/<int:delivery_id>/full-information', methods=['GET'])
def handleDeliveryByIdFullInfo(delivery_id):
    if request.method == 'GET':
        return BaseDelivery().getDeliveryByIdFullInfo(delivery_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Delivery/deliveries/<int:delivery_id>/status', methods=['PUT'])
def handleDeliveryByStatus(delivery_id):
    if request.method == 'PUT':
        return BaseDelivery().updateDeliveryStatus(delivery_id, request.json)
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


@app.route('/Dispensary/dispensaries/<int:dispensary_id>', methods=['GET', 'DELETE', 'PUT'])
def handleDispensaryById(dispensary_id):
    if request.method == 'GET':
        return BaseDispensary().getDispensaryById(dispensary_id)
    elif request.method == 'DELETE':
        return BaseDispensary().deleteDispensary(dispensary_id)
    elif request.method == 'PUT':
        return BaseDispensary().updateDispensaryData(dispensary_id, request.json)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Dispensary/dispensaries/<int:dispensary_id>/item/<int:item_id>', methods=['GET'])
def handleDispensaryItemsById(dispensary_id, item_id):
    if request.method == 'GET':
        return BaseItem().getItemAtDispensary(dispensary_id, item_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Dispensary/dispensaries/<int:dispensary_id>/items', methods=['GET', 'POST'])
def handleDispensaryItems(dispensary_id):
    if request.method == 'GET':
        return BaseItem().getAllItemsAtDispensary(dispensary_id)
    elif request.method == 'POST':
        return BaseItem().createItem(dispensary_id, request.json)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Dispensary/dispensaries/<int:dispensary_id>/purchases', methods=['GET'])
def handleDispensaryPurchases(dispensary_id):
    if request.method == 'GET':
        return BasePurchase().getAllPurchasesAtDispensary(dispensary_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Dispensary/dispensaries/<int:dispensary_id>/purchase/<int:purchase_id>', methods=['GET'])
def handleDispensaryItemsByDispensaryId(dispensary_id, purchase_id):
    if request.method == 'GET':
        return BasePurchase().getPurchaseByIdAtDispensary(dispensary_id, purchase_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Dispensary/dispensaries/<int:dispensary_id>/<int:item_id>', methods=['GET', 'DELETE', 'PUT'])
def handleItemById(dispensary_id, item_id):
    if request.method == 'GET':
        return BaseItem().getItemAtDispensary(dispensary_id, item_id)
    elif request.method == 'DELETE':
        return BaseItem().deleteItemAtDispensary(dispensary_id, item_id)
    elif request.method == 'PUT':
        return BaseItem().updateItemData(dispensary_id, item_id, request.json)
    else:
        return jsonify("Method Not Allowed"), 405


# TODO: Endpoint to update picture for both item and dispensary

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


@app.route('/Driver/drivers/<int:driver_id>', methods=['GET', 'DELETE', 'PUT'])
def handleDriverById(driver_id):
    if request.method == 'GET':
        return BaseDriver().getDriverById(driver_id)
    elif request.method == 'DELETE':
        return BaseDriver().deleteDriver(driver_id)
    elif request.method == 'PUT':
        return BaseDriver().updateDriverData(driver_id, request.json)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Driver/drivers/<int:driver_id>/deliveries', methods=['GET', 'POST'])
def handleDriverDeliveries(driver_id):
    if request.method == 'GET':
        return BaseDriver().getAllDriverDeliveries(driver_id)
    elif request.method == 'POST':
        return BaseDelivery().updateDeliveryDriver(request.json, driver_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Driver/drivers/<int:driver_id>/deliveries/past', methods=['GET'])
def handlePastDriverDeliveries(driver_id):
    if request.method == 'GET':
        return BaseDriver().getAllPastDriverDeliveries(driver_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Driver/drivers/<int:driver_id>/register-vehicle', methods=['POST'])
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


@app.route('/Item/items/filter/<item_filter>', methods=['GET'])
def handleItemsByName(item_filter):
    if request.method == 'GET':
        return BaseItem().getItemByFilter(item_filter)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Item/items/category/<item_category>', methods=['GET'])
def handleItemsByCategory(item_category):
    if request.method == 'GET':
        return BaseItem().getItemByCategory(item_category)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Item/items/price/', methods=['GET'])
def handleItemsByPriceRange():
    if request.method == 'GET':
        return BaseItem().getItemByPriceRange(request.json)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Item/items/active', methods=['GET'])
def handleActiveItems():
    if request.method == 'GET':
        return BaseItem().getAllActiveItems()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Item/items/<int:item_id>/quantity', methods=['PUT'])
def handleItemQuantity(item_id):
    if request.method == 'PUT':
        return BaseItem().updateItemQuantity(item_id, request.json)
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


@app.route('/Purchase/purchases/<int:purchase_id>', methods=['GET', 'PUT'])
def handlePurchasesById(purchase_id):
    if request.method == 'GET':
        return BasePurchase().getPurchaseById(purchase_id)
    elif request.method == 'PUT':
        return BasePurchase().updatePurchase(purchase_id, request.json)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Purchase/purchases/<int:purchase_id>/completed', methods=['PUT'])
def handleCompletedPurchasesById(purchase_id):
    if request.method == 'PUT':
        return BasePurchase().markPurchaseAsCompleted(purchase_id)
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


@app.route('/User/users/<int:user_id>', methods=['GET', 'DELETE', 'PUT'])
def handleUsersById(user_id):
    if request.method == 'GET':
        return BaseUser().getUserById(user_id)
    elif request.method == 'DELETE':
        return BaseUser().deleteUser(user_id)
    elif request.method == 'PUT':
        return BaseUser().updateUserData(user_id, request.json)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/User/users/<int:user_id>/purchases', methods=['GET', 'POST'])
def handleUserPurchasesById(user_id):
    if request.method == 'GET':
        return BasePurchase().getPurchasesByUser(user_id)
    elif request.method == 'POST':
        return BasePurchase().createPurchase(user_id, request.json)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/User/users/<int:user_id>/purchases/past', methods=['GET'])
def handlePastUserPurchasesById(user_id):
    if request.method == 'GET':
        return BasePurchase().getPastPurchasesByUser(user_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/User/users/<int:user_id>/purchases/delivery', methods=['GET'])
def handleUserDeliveriesById(user_id):
    if request.method == 'GET':
        return BaseDelivery().getDeliveryByUser(user_id)
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


@app.route('/Vehicle/vehicles/<int:vehicle_id>', methods=['GET', 'DELETE'])
def handleVehicleById(vehicle_id):
    if request.method == 'GET':
        return BaseVehicle().getVehicleById(vehicle_id)
    elif request.method == 'DELETE':
        return BaseVehicle().deleteVehicle(vehicle_id)
    else:
        return jsonify("Method Not Allowed"), 405


# --------------------------------------------------------------------------------------
# Statistics
# --------------------------------------------------------------------------------------
@app.route('/Statistics/Dispensary/<int:dispensary_id>/total-purchases', methods=['GET'])
def handleTotalOfPurchases(dispensary_id):
    if request.method == 'GET':
        return BasePurchase().getTotalOfPurchasesByDispensary(dispensary_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Statistics/Dispensary/<int:dispensary_id>/items-in-stock', methods=['GET'])
def handleTotalOfItemsInStock(dispensary_id):
    if request.method == 'GET':
        return BaseItem().getTotalOfItemsInStockAtDispensary(dispensary_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Statistics/Dispensary/<int:dispensary_id>/items-out-of-stock', methods=['GET'])
def handleTotalOfItemsOutOfStock(dispensary_id):
    if request.method == 'GET':
        return BaseItem().getTotalOfItemsOutOfStockAtDispensary(dispensary_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Statistics/Dispensary/<int:dispensary_id>/most-sold-item', methods=['GET'])
def HandleMostSoldItemByDispensary(dispensary_id):
    if request.method == 'GET':
        return BasePurchase().getMostSoldItemAtDispensary(dispensary_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/Statistics/Dispensary/<int:dispensary_id>/least-sold-item', methods=['GET'])
def HandleLeastSoldItemByDispensary(dispensary_id):
    if request.method == 'GET':
        return BasePurchase().getLeastSoldItemAtDispensary(dispensary_id)
    else:
        return jsonify("Method Not Allowed"), 405


# --------------------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------------------
if __name__ == 'main':
    app.run()
