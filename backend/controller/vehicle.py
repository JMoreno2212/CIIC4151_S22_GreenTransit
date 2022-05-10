from flask import jsonify

from backend.model.license import LicenseDAO
from backend.model.vehicle import VehicleDAO


def build_vehicle_map_dict(row):
    result = {'vehicle_id': row[0], 'vehicle_plate': row[1], 'vehicle_brand': row[2], 'vehicle_model': row[3],
              'vehicle_year': row[4], 'driver_id': row[5], 'license_id': row[6], 'vehicle_active': row[7]}
    return result


def build_vehicle_attr_dict(vehicle_id, vehicle_plate, vehicle_brand, vehicle_model, vehicle_year, driver_id,
                            license_id, vehicle_active):
    result = {'vehicle_id': vehicle_id, 'vehicle_plate': vehicle_plate, 'vehicle_brand': vehicle_brand,
              'vehicle_model': vehicle_model, 'vehicle_year': vehicle_year, 'driver_id': driver_id,
              'license_id': license_id, 'vehicle_active': vehicle_active}
    return result


class BaseVehicle:

    def createVehicle(self, driver_id, json):
        vehicle_plate = json['vehicle_plate']
        vehicle_brand = json['vehicle_brand']
        vehicle_model = json['vehicle_model']
        vehicle_year = json['vehicle_year']
        license_type = json['registration_type']
        license_name = json['license_name']
        license_expiration = json['license_expiration']
        license_file = json['license_file']
        vehicle_dao = VehicleDAO()
        license_dao = LicenseDAO()
        driver_has_vehicle = vehicle_dao.getVehicleByDriver(driver_id)
        if driver_has_vehicle is not None:
            return jsonify("Driver already has a vehicle registered"), 409
        existing_license = license_dao.getLicenseByName(license_name)
        if not existing_license:  # Vehicle License is not registered
            license_id = license_dao.createLicense(license_type, license_name, license_expiration, license_file)
            vehicle_id = vehicle_dao.createVehicle(vehicle_plate, vehicle_brand, vehicle_model, vehicle_year,
                                                   driver_id, license_id)
            result = build_vehicle_attr_dict(vehicle_id, vehicle_plate, vehicle_brand, vehicle_model, vehicle_year,
                                             driver_id, license_id, True)
            return jsonify(result), 201
        else:
            return jsonify("Vehicle is already registered"), 409

    def getAllVehicles(self):
        vehicle_dao = VehicleDAO()
        vehicles_list = vehicle_dao.getAllVehicles()
        if not vehicles_list:  # Vehicle List is empty
            return jsonify("No Vehicles Found"), 404
        else:
            result_list = []
            for row in vehicles_list:
                obj = build_vehicle_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list), 200

    def getAllActiveVehicles(self):
        vehicle_dao = VehicleDAO()
        vehicles_list = vehicle_dao.getAllActiveVehicles()
        if not vehicles_list:  # Vehicle List is empty
            return jsonify("No Vehicles Found"), 404
        else:
            result_list = []
            for row in vehicles_list:
                obj = build_vehicle_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list), 200

    def getVehicleById(self, vehicle_id):
        vehicle_dao = VehicleDAO()
        vehicle_tuple = vehicle_dao.getVehicleById(vehicle_id)
        if not vehicle_tuple:  # Vehicle Not Found
            return jsonify("Vehicle Not Found"), 404
        else:
            result = build_vehicle_map_dict(vehicle_tuple)
        return jsonify(result), 200

    # def updateVehicle(self, vehicle_id, json):
    #     vehicle_dao = VehicleDAO()
    #     vehicle_plate = json['vehicle_plate']
    #     vehicle_brand = json['vehicle_brand']
    #     vehicle_model = json['vehicle_model']
    #     vehicle_year = json['vehicle_year']
    #     driver_id = json['driver_id']
    #     new_email = user_dao.getUserByEmail(user_email)
    #     # New email doesn't exist or is the same as current
    #     if (not new_email) or (user_email == user_dao.getUserById(user_id)[5]):
    #         user_dao.updateUser(user_id, user_phone, user_email, user_password)
    #         updated_user = user_dao.getUserById(user_id)
    #         result = build_user_map_dict(updated_user)
    #         return jsonify(result), 200
    #     else:
    #         return jsonify("Email address is already in use"), 409

    def deleteVehicle(self, vehicle_id):
        vehicle_dao = VehicleDAO()
        vehicle_dao.deleteVehicle(vehicle_id)
        deleted_vehicle = vehicle_dao.getVehicleById(vehicle_id)
        deleted_license_id = deleted_vehicle[6]
        license_dao = LicenseDAO()
        license_dao.deleteLicense(deleted_license_id)
        result = build_vehicle_map_dict(deleted_vehicle)
        return jsonify(result), 200
