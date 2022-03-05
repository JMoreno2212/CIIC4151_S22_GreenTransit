from flask import jsonify

from backend.model.delivery import DeliveryDAO


def build_delivery_map_dict(row):
    result = {'delivery_id': row[0], 'delivery_date': row[1], 'delivery_price': row[2], 'delivery_location': row[3],
              'driver_id': row[4], 'vehicle_id': row[5], 'purchase_id': row[6]}
    return result


class BaseDelivery:

    def getAllDeliveries(self):
        delivery_dao = DeliveryDAO()
        delivery_list = delivery_dao.getAllDeliveries()
        if not delivery_list:  # Delivery List is empty
            return jsonify("No Deliveries Found"), 404
        else:
            result_list = []
            for row in delivery_list:
                obj = build_delivery_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list), 200

    def getDeliveryById(self, delivery_id):
        delivery_dao = DeliveryDAO()
        delivery_tuple = delivery_dao.getDeliveryById(delivery_id)
        if not delivery_tuple:  # Delivery Not Found
            return jsonify("Delivery Not Found"), 404
        else:
            result = build_delivery_map_dict(delivery_tuple)
            return jsonify(result), 200
