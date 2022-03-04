from flask import jsonify

from backend.model.dispensary import DispensaryDAO
from backend.model.item import ItemDAO
from backend.model.user import UserDAO
from backend.model.vehicle import VehicleDAO


def build_vehicle_map_dict(row):
    result = {'vehicle_id': row[0], 'vehicle_plate': row[1], 'vehicle_brand': row[2], 'vehicle_model': row[3],
              'vehicle_year': row[4], 'driver_id': row[5], 'vehicle_active': row[6]}
    return result


class BaseVehicle:
    def getAllVehicles(self):
        vehicle_dao = VehicleDAO()
        vehicles_list = vehicle_dao.getAllVehicles()
        if not vehicles_list:  # Item List is empty
            return jsonify("No Vehicles Found"), 404
        else:
            result_list = []
            for row in vehicles_list:
                obj = build_vehicle_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list), 200
