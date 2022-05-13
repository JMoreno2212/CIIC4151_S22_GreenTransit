import os

from flask import jsonify

from backend.model.driver import DriverDAO
from backend.model.license import LicenseDAO
from backend.model.vehicle import VehicleDAO
from backend.aws_management import AWSHandler


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

    def createDriver(self, files):
        driver_first_name = files['registration_first_name']
        driver_last_name = files['registration_last_name']
        driver_birth_date = files['registration_birth_date']
        driver_phone = files['registration_phone']
        driver_email = files['registration_email']
        driver_password = files['registration_password']
        driver_driving_license = files['driver_driving_license']
        driver_driving_license.save("uploads/" + driver_driving_license.filename)
        driver_gmp_certificate = files['driver_gmp_certificate']
        driver_gmp_certificate.save("uploads/" + driver_gmp_certificate.filename)
        driver_dispensary_technician = files['driver_dispensary_technician']
        driver_dispensary_technician.save("uploads/" + driver_dispensary_technician.filename)
        license_type = "Occupational"  # This occurs since Driver's License is asked on a separate field
        license_name = files['license_name']
        license_expiration = files['license_expiration']
        license_file = files['license_file']
        license_file.save("uploads/" + license_file.filename)
        driver_picture = files['registration_picture']
        driver_picture.save("uploads/" + driver_picture.filename)
        driver_dao = DriverDAO()
        existing_driver = driver_dao.getDriverByEmail(driver_email)
        license_dao = LicenseDAO()
        existing_license = license_dao.getLicenseByName(license_name)
        if not existing_driver and not existing_license:  # Driver with that email and license does not exist
            aws_handler = AWSHandler()

            license_file_name = 'license_file' + os.getenv('FILE_COUNTER') + '.pdf'
            uploaded_license = aws_handler.upload_file(license_file, os.getenv('BUCKET_NAME'), license_file_name)
            os.environ['FILE_COUNTER'] = str(int(os.getenv('FILE_COUNTER')) + 1)  # Increment File Counter

            driver_picture_name = 'driver_picture' + os.getenv('FILE_COUNTER') + '.png'
            uploaded_picture = aws_handler.upload_file(driver_picture, os.getenv('BUCKET_NAME'), driver_picture_name)
            os.environ['FILE_COUNTER'] = str(int(os.getenv('FILE_COUNTER')) + 1)  # Increment File Counter

            driver_gmp_certificate_name = 'driver_gmp_certificate' + os.getenv('FILE_COUNTER') + '.pdf'
            uploaded_certificate = aws_handler.upload_file(driver_gmp_certificate, os.getenv('BUCKET_NAME'),
                                                           driver_gmp_certificate_name)
            os.environ['FILE_COUNTER'] = str(int(os.getenv('FILE_COUNTER')) + 1)  # Increment File Counter

            driver_dispensary_technician_name = 'driver_dispensary_technician' + os.getenv('FILE_COUNTER') + '.pdf'
            uploaded_technician = aws_handler.upload_file(driver_dispensary_technician, os.getenv('BUCKET_NAME'),
                                                          driver_dispensary_technician_name)
            os.environ['FILE_COUNTER'] = str(int(os.getenv('FILE_COUNTER')) + 1)  # Increment File Counter

            driver_driving_license_name = 'driver_driving_license.' + os.getenv('FILE_COUNTER') + 'pdf'
            uploaded_driver_license = aws_handler.upload_file(driver_driving_license, os.getenv('BUCKET_NAME'),
                                                              driver_driving_license_name)
            os.environ['FILE_COUNTER'] = str(int(os.getenv('FILE_COUNTER')) + 1)  # Increment File Counter

            # Upload failed
            if not uploaded_license or not uploaded_picture or not uploaded_certificate or not uploaded_technician \
                    or not uploaded_driver_license:
                aws_handler.delete_file(license_name, os.getenv('BUCKET_NAME'))
                aws_handler.delete_file(driver_picture, os.getenv('BUCKET_NAME'))
                aws_handler.delete_file(driver_gmp_certificate, os.getenv('BUCKET_NAME'))
                aws_handler.delete_file(driver_driving_license, os.getenv('BUCKET_NAME'))
                os.environ['FILE_COUNTER'] = str(int(os.getenv('FILE_COUNTER')) - 5)  # Decrease File Counter by 5
                return jsonify("Error reading input files"), 409
            license_id = license_dao.createLicense(license_type, license_name, license_expiration,
                                                   license_file_name)
            driver_id = driver_dao.createDriver(driver_first_name, driver_last_name, driver_birth_date, driver_phone,
                                                driver_email, driver_password, driver_driving_license_name,
                                                driver_gmp_certificate_name, driver_dispensary_technician_name,
                                                license_id, driver_picture_name)
            result = build_driver_attr_dict(driver_id, driver_first_name, driver_last_name, driver_birth_date,
                                            driver_phone, driver_email, driver_password,
                                            driver_driving_license_name, driver_gmp_certificate_name,
                                            driver_dispensary_technician_name, license_id, True,
                                            driver_picture_name)
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

    def getAllPastDriverDeliveries(self, driver_id):
        driver_dao = DriverDAO()
        driver_deliveries = driver_dao.getAllPastDriverDeliveries(driver_id)
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

    def updateDriverPicture(self, driver_id, files):
        driver_dao = DriverDAO()
        driver_picture = files['driver_picture']
        aws_handler = AWSHandler()
        driver_picture.save("uploads/" + driver_picture.filename)
        driver_picture_name = 'driver_picture' + os.getenv('FILE_COUNTER') + '.png'
        uploaded_picture = aws_handler.upload_file(driver_picture, os.getenv('BUCKET_NAME'), driver_picture_name)
        if not uploaded_picture:  # Upload failed
            return jsonify("Error reading input files"), 409
        os.environ['FILE_COUNTER'] = str(int(os.getenv('FILE_COUNTER')) + 1)  # Increment File Counter
        driver_dao.updateDriverPicture(driver_id, driver_picture.filename)
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
