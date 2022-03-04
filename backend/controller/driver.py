from flask import jsonify

from backend.model.dispensary import DispensaryDAO
from backend.model.driver import DriverDAO
from backend.model.user import UserDAO


def build_driver_map_dict(row):
    result = {'driver_id': row[0], 'driver_first_name': row[1], 'driver_last_name': row[2], 'driver_phone': row[3],
              'driver_email': row[4], 'driver_password': row[5], 'license_id': row[6], 'driver_active': row[7]}
    return result


class BaseDriver:
    def getAllDrivers(self):
        driver_dao = DriverDAO()
        drivers_list = driver_dao.getAllDrivers()
        if not drivers_list:  # Drivers List is empty
            return jsonify("No Drivers Found"), 404
        else:
            result_list = []
            for row in drivers_list:
                obj = build_driver_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list), 200
