from flask import jsonify

from backend.model.delivery import DeliveryDAO
from backend.model.driver import DriverDAO
from backend.model.purchase import PurchaseDAO
from backend.model.vehicle import VehicleDAO


def build_delivery_map_dict(row):
    result = {'delivery_id': row[0], 'delivery_date': row[1], 'delivery_price': row[2], 'delivery_direction': row[3],
              'delivery_municipality': row[4], 'delivery_zipcode': row[5], 'delivery_status': row[6],
              'driver_id': row[7], 'vehicle_id': row[8], 'purchase_id': row[9]}
    return result


def build_delivery_all_info_map_dict(row):
    result = {'delivery_id': row[0], 'driver_id': row[1], 'purchase_id': row[2], 'purchase_number': row[3],
              'purchase_date': row[4], 'user_id': row[5], 'user_first_name': row[6], 'user_last_name': row[7],
              'user_phone': row[8], 'user_email': row[9], 'delivery_direction': row[10],
              'delivery_municipality': row[11], 'dispensary_id': row[12], 'dispensary_name': row[13],
              'dispensary_phone': row[14], 'dispensary_email': row[15], 'dispensary_direction': row[16],
              'dispensary_municipality': row[17]}
    return result


def build_delivery_attr_dict(delivery_id, delivery_date, delivery_price, delivery_direction, delivery_municipality,
                             delivery_zipcode, delivery_status, driver_id, vehicle_id, purchase_id):
    result = {'delivery_id': delivery_id, 'delivery_date': delivery_date, 'delivery_price': delivery_price,
              'delivery_direction': delivery_direction, 'delivery_municipality': delivery_municipality,
              'delivery_zipcode': delivery_zipcode, 'delivery_status': delivery_status, 'driver_id': driver_id,
              'vehicle_id': vehicle_id, 'purchase_id': purchase_id}
    return result


class BaseDelivery:

    def createDelivery(self, json):
        delivery_date = json['delivery_date']
        delivery_price = json['delivery_price']
        delivery_direction = json['delivery_direction']
        delivery_municipality = json['delivery_municipality']
        delivery_zipcode = json['delivery_zipcode']
        driver_id = json['driver_id']
        vehicle_id = json['vehicle_id']
        purchase_id = json['purchase_id']

        delivery_dao = DeliveryDAO()
        driver_dao = DriverDAO()
        existing_driver = driver_dao.getDriverById(driver_id)
        vehicle_dao = VehicleDAO()
        existing_vehicle = vehicle_dao.getVehicleById(vehicle_id)
        purchase_dao = PurchaseDAO()
        existing_purchase = purchase_dao.getPurchaseById(purchase_id)

        if not existing_driver:
            return jsonify("Driver does not exist"), 404
        if not existing_vehicle:
            return jsonify("Vehicle does not exist"), 404
        if not existing_purchase:
            return jsonify("Purchase does not exist"), 404

        delivery_id = delivery_dao.createDelivery(delivery_date, delivery_price, delivery_direction,
                                                  delivery_municipality, delivery_zipcode, driver_id, vehicle_id,
                                                  purchase_id)
        result = build_delivery_attr_dict(delivery_id, delivery_date, delivery_price, delivery_direction,
                                          delivery_municipality, delivery_zipcode, "Awaiting Shipment", driver_id,
                                          vehicle_id, purchase_id)
        return jsonify(result), 200

    def getAllDeliveriesBasicInfo(self):
        delivery_dao = DeliveryDAO()
        delivery_list = delivery_dao.getAllDeliveriesBasicInfo()
        if not delivery_list:  # Delivery List is empty
            return jsonify("No Deliveries Found"), 404
        else:
            result_list = []
            for row in delivery_list:
                obj = build_delivery_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list), 200

    def getAllDeliveriesFullInfo(self):
        delivery_dao = DeliveryDAO()
        delivery_list = delivery_dao.getAllDeliveriesFullInfo()
        if not delivery_list:  # Delivery List is empty
            return jsonify("No Deliveries Found"), 404
        else:
            result_list = []
            for row in delivery_list:
                obj = build_delivery_all_info_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list), 200

    def getAllDeliveriesWithoutDriver(self):
        delivery_dao = DeliveryDAO()
        delivery_list = delivery_dao.getAllDeliveriesWithoutDriver()
        if not delivery_list:  # Delivery List is empty
            return jsonify("No Deliveries Found"), 404
        else:
            result_list = []
            for row in delivery_list:
                obj = build_delivery_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list), 200

    def getDeliveryByIdBasicInfo(self, delivery_id):
        delivery_dao = DeliveryDAO()
        delivery_tuple = delivery_dao.getDeliveryByIdBasicInfo(delivery_id)
        if not delivery_tuple:  # Delivery Not Found
            return jsonify("Delivery Not Found"), 404
        else:
            result = build_delivery_map_dict(delivery_tuple)
            return jsonify(result), 200

    def getDeliveryByIdFullInfo(self, delivery_id):
        delivery_dao = DeliveryDAO()
        delivery_tuple = delivery_dao.getDeliveryByIdFullInfo(delivery_id)
        if not delivery_tuple:  # Delivery Not Found
            return jsonify("Delivery Not Found"), 404
        else:
            result = build_delivery_all_info_map_dict(delivery_tuple)
            return jsonify(result), 200

    def getDeliveryByUser(self, user_id):
        delivery_dao = DeliveryDAO()
        delivery_tuple = delivery_dao.getDeliveryByUser(user_id)
        if not delivery_tuple:  # Delivery Not Found
            return jsonify("Delivery Not Found"), 404
        else:
            result = build_delivery_map_dict(delivery_tuple)
            return jsonify(result), 200

    def updateDeliveryInformation(self, delivery_id, json):
        delivery_dao = DeliveryDAO()
        delivery_date = json['delivery_date']
        delivery_direction = json['delivery_direction']
        delivery_municipality = json['delivery_municipality']
        delivery_zipcode = json['delivery_zipcode']
        delivery_dao.updateDeliveryInformation(delivery_id, delivery_date, delivery_direction, delivery_municipality,
                                               delivery_zipcode)
        updated_delivery = delivery_dao.getDeliveryByIdBasicInfo(delivery_id)
        result = build_delivery_map_dict(updated_delivery)
        return jsonify(result), 200

    def updateDeliveryStatus(self, delivery_id, json):
        delivery_dao = DeliveryDAO()
        delivery_status = json['delivery_status']
        delivery_dao.updateDeliveryStatus(delivery_id, delivery_status)
        updated_delivery = delivery_dao.getDeliveryByIdBasicInfo(delivery_id)
        result = build_delivery_map_dict(updated_delivery)
        return jsonify(result), 200

    def updateDeliveryDriver(self, json, driver_id):
        delivery_dao = DeliveryDAO()
        delivery_id = json['delivery_id']
        delivery_dao.updateDeliveryDriver(delivery_id, driver_id)
        updated_delivery = delivery_dao.getDeliveryByIdBasicInfo(delivery_id)
        result = build_delivery_map_dict(updated_delivery)
        return jsonify(result), 200
