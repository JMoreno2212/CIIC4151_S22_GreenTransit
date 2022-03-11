from flask import jsonify

from backend.model.driver import DriverDAO


def build_driver_map_dict(row):
    result = {'driver_id': row[0], 'driver_first_name': row[1], 'driver_last_name': row[2], 'driver_phone': row[3],
              'driver_email': row[4], 'driver_password': row[5], 'license_id': row[6], 'driver_active': row[7]}
    return result


def build_driver_attr_dict(driver_id, driver_first_name, driver_last_name, driver_phone, driver_email, driver_password,
                           license_id, driver_active):
    result = {'driver_id': driver_id, 'driver_first_name': driver_first_name, 'driver_last_name': driver_last_name,
              'driver_phone': driver_phone, 'driver_email': driver_email, 'driver_password': driver_password,
              'license_id': license_id, 'driver_active': driver_active}
    return result


class BaseDriver:

    def createDriver(self, json):
        driver_first_name = json['driver_first_name']
        driver_last_name = json['driver_last_name']
        driver_phone = json['driver_phone']
        driver_email = json['driver_email']
        driver_password = json['driver_password']
        license_id = json['license_id']
        driver_dao = DriverDAO()
        existing_driver = driver_dao.getDriverByEmail(driver_email)
        if not existing_driver:  # Driver with that email does not exist
            driver_id = driver_dao.createDriver(driver_first_name, driver_last_name, driver_phone,
                                                driver_email, driver_password, license_id)
            result = build_driver_attr_dict(driver_id, driver_first_name, driver_last_name, driver_phone, driver_email,
                                            driver_password, license_id, True)
            return jsonify(result), 201
        else:
            return jsonify("An user with that email already exists"), 409

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

    def getAllActiveDrivers(self):
        driver_dao = DriverDAO()
        drivers_list = driver_dao.getAllActiveDrivers()
        if not drivers_list:  # Drivers List is empty
            return jsonify("No Drivers Found"), 404
        else:
            result_list = []
            for row in drivers_list:
                obj = build_driver_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list), 200

    def getDriverById(self, driver_id):
        driver_dao = DriverDAO()
        driver_tuple = driver_dao.getDriverById(driver_id)
        if not driver_tuple:  # Driver Not Found
            return jsonify("Driver Not Found"), 404
        else:
            result = build_driver_map_dict(driver_tuple)
        return jsonify(result), 200

    def verifyDriverLogin(self, json):
        driver_email = json['login_email']
        driver_password = json['login_password']
        driver_dao = DriverDAO()
        valid_driver = driver_dao.verifyDriverLogin(driver_email, driver_password)
        if not valid_driver:
            return jsonify("Username or Password entered incorrectly"), 404
        else:
            return jsonify("Driver logged in successfully", valid_driver[0], valid_driver[4]), 200  # Returns ID & Email
