from flask import jsonify

from backend.model.driver import DriverDAO
from backend.model.license import LicenseDAO


def build_driver_map_dict(row):
    result = {'driver_id': row[0], 'driver_first_name': row[1], 'driver_last_name': row[2], 'driver_birth_date': row[3],
              'driver_phone': row[4], 'driver_email': row[5], 'driver_password': row[6],
              'driver_driving_license': row[7], 'driver_gmp_certificate': row[8],
              'driver_dispensary_technician': row[9], 'occupational_license_id': row[10], 'driver_active': row[11]}
    return result


def build_driver_attr_dict(driver_id, driver_first_name, driver_last_name, driver_birth_date, driver_phone,
                           driver_email, driver_password, driver_driving_license, driver_gmp_certificate,
                           driver_dispensary_technician, occupational_license_id, driver_active):
    result = {'driver_id': driver_id, 'driver_first_name': driver_first_name, 'driver_last_name': driver_last_name,
              'driver_birth_date': driver_birth_date, 'driver_phone': driver_phone, 'driver_email': driver_email,
              'driver_password': driver_password, 'driver_driving_license': driver_driving_license,
              'driver_gmp_certificate': driver_gmp_certificate,
              'driver_dispensary_technician': driver_dispensary_technician,
              'occupational_license_id': occupational_license_id, 'driver_active': driver_active}
    return result


class BaseDriver:

    def createDriver(self, json):
        driver_first_name = json['registration_first_name']
        driver_last_name = json['registration_last_name']
        driver_birth_date = json['registration_birth_date']
        driver_phone = json['registration_phone']
        driver_email = json['registration_email']
        driver_password = json['registration_password']
        driver_driving_license = json['driver_driving_license']
        driver_gmp_certificate = json['driver_gmp_certificate']
        driver_dispensary_technician = json['driver_dispensary_technician']
        license_type = "Occupational"  # This occurs since Driver's License is asked on a separate field
        license_name = json['license_name']
        license_expiration = json['license_expiration']
        license_file = json['license_file']
        driver_dao = DriverDAO()
        existing_driver = driver_dao.getDriverByEmail(driver_email)
        license_dao = LicenseDAO()
        existing_license = license_dao.getLicenseByName(license_name)
        if not existing_driver and not existing_license:  # Driver with that email and license does not exist
            license_id = license_dao.createLicense(license_type, license_name, license_expiration, license_file)
            driver_id = driver_dao.createDriver(driver_first_name, driver_last_name, driver_birth_date, driver_phone,
                                                driver_email, driver_password, driver_driving_license,
                                                driver_gmp_certificate, driver_dispensary_technician, license_id)
            result = build_driver_attr_dict(driver_id, driver_first_name, driver_last_name, driver_birth_date,
                                            driver_phone, driver_email, driver_password, driver_driving_license,
                                            driver_gmp_certificate, driver_dispensary_technician, license_id, True)
            return jsonify(result), 201
        else:
            return jsonify("User already exists"), 409

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
