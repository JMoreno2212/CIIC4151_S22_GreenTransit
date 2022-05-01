from flask import jsonify

from backend.model.driver import DriverDAO
from backend.model.license import LicenseDAO
from backend.model.vehicle import VehicleDAO


def build_driver_map_dict(row):
    result = {'driver_id': row[0], 'driver_first_name': row[1], 'driver_last_name': row[2], 'driver_birth_date': row[3],
              'driver_phone': row[4], 'driver_email': row[5], 'driver_password': row[6],
              'driver_driving_license': row[7], 'driver_gmp_certificate': row[8],
              'driver_dispensary_technician': row[9], 'occupational_license_id': row[10], 'driver_active': row[11],
              'driver_picture': row[12]}
    return result


def build_driver_attr_dict(driver_id, driver_first_name, driver_last_name, driver_birth_date, driver_phone,
                           driver_email, driver_password, driver_driving_license, driver_gmp_certificate,
                           driver_dispensary_technician, occupational_license_id, driver_active, driver_picture):
    result = {'driver_id': driver_id, 'driver_first_name': driver_first_name, 'driver_last_name': driver_last_name,
              'driver_birth_date': driver_birth_date, 'driver_phone': driver_phone, 'driver_email': driver_email,
              'driver_password': driver_password, 'driver_driving_license': driver_driving_license,
              'driver_gmp_certificate': driver_gmp_certificate,
              'driver_dispensary_technician': driver_dispensary_technician,
              'occupational_license_id': occupational_license_id, 'driver_active': driver_active,
              'driver_picture': driver_picture}
    return result


def build_driver_delivery_map_dict(row):
    result = {'delivery_id': row[0], 'driver_id': row[1], 'purchase_id': row[2], 'purchase_number': row[3],
              'purchase_date': row[4], 'user_id': row[5], 'user_first_name': row[6], 'user_last_name': row[7],
              'user_phone': row[8], 'user_email': row[9], 'delivery_direction': row[10],
              'delivery_municipality': row[11], 'dispensary_id': row[12], 'dispensary_name': row[13],
              'dispensary_phone': row[14], 'dispensary_email': row[15], 'dispensary_direction': row[16],
              'dispensary_municipality': row[17], 'driver_first_name': row[18],
              'driver_last_name': row[19], 'delivery_status': row[20]}
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
        driver_picture = json['registration_picture']
        driver_dao = DriverDAO()
        existing_driver = driver_dao.getDriverByEmail(driver_email)
        license_dao = LicenseDAO()
        existing_license = license_dao.getLicenseByName(license_name)
        if not existing_driver and not existing_license:  # Driver with that email and license does not exist
            license_id = license_dao.createLicense(license_type, license_name, license_expiration, license_file)
            driver_id = driver_dao.createDriver(driver_first_name, driver_last_name, driver_birth_date, driver_phone,
                                                driver_email, driver_password, driver_driving_license,
                                                driver_gmp_certificate, driver_dispensary_technician, license_id,
                                                driver_picture)
            result = build_driver_attr_dict(driver_id, driver_first_name, driver_last_name, driver_birth_date,
                                            driver_phone, driver_email, driver_password, driver_driving_license,
                                            driver_gmp_certificate, driver_dispensary_technician, license_id, True,
                                            driver_picture)
            return jsonify(result), 201
        else:
            return jsonify("User already exists"), 409

    def deleteDriver(self, driver_id):
        driver_dao = DriverDAO()
        driver_dao.deleteDriver(driver_id)
        deleted_driver = driver_dao.getDriverById(driver_id)
        deleted_license_id = deleted_driver[10]
        license_dao = LicenseDAO()
        license_dao.deleteLicense(deleted_license_id)
        vehicle_dao = VehicleDAO()
        deleted_vehicle_id = vehicle_dao.getVehicleByDriver(driver_id)
        vehicle_dao.deleteVehicle(deleted_vehicle_id)
        result = build_driver_map_dict(deleted_driver)
        return jsonify(result), 200

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

    def getAllDriverDeliveries(self, driver_id):
        driver_dao = DriverDAO()
        driver_deliveries = driver_dao.getAllDriverDeliveries(driver_id)
        if not driver_deliveries:  # Drivers List is empty
            return jsonify("No Deliveries Found"), 404
        else:
            result_list = []
            for row in driver_deliveries:
                obj = build_driver_delivery_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list), 200

    def resetPassword(self, json):
        driver_dao = DriverDAO()
        driver_email = json['email']
        new_password = json['password']
        reset_password = driver_dao.resetPassword(driver_email, new_password)
        if not reset_password:  # No driver password was reset
            return None
        else:
            updated_driver = driver_dao.getDriverByEmail(driver_email)
            result = build_driver_map_dict(updated_driver)
            return jsonify(result), 200

    def updateDriverData(self, driver_id, json):
        driver_dao = DriverDAO()
        driver_phone = json['driver_phone']
        driver_email = json['driver_email']
        driver_password = json['driver_password']
        new_email = driver_dao.getDriverByEmail(driver_email)
        # New email doesn't exist or is the same as current
        if (not new_email) or (driver_email == driver_dao.getDriverById(driver_id)[5]):
            driver_dao.updateDriverData(driver_id, driver_phone, driver_email, driver_password)
            updated_driver = driver_dao.getDriverById(driver_id)
            result = build_driver_map_dict(updated_driver)
            return jsonify(result), 200
        else:
            return jsonify("Email address is already in use"), 409

    def updateDriverPicture(self, driver_id, json):
        driver_dao = DriverDAO()
        driver_picture = json['driver_picture']
        driver_dao.updateDriverPicture(driver_id, driver_picture)
        updated_driver = driver_dao.getDriverById(driver_id)
        result = build_driver_map_dict(updated_driver)
        return jsonify(result), 200

    def verifyDriverLogin(self, json):
        driver_email = json['login_email']
        driver_password = json['login_password']
        driver_dao = DriverDAO()
        valid_driver = driver_dao.verifyDriverLogin(driver_email, driver_password)
        if not valid_driver:
            return None
        else:
            # Returns ID, Email & Type
            return jsonify("Driver logged in successfully", valid_driver[0], valid_driver[4], "Driver"), 200
