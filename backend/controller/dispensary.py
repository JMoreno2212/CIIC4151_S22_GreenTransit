from flask import jsonify

from backend.model.dispensary import DispensaryDAO
from backend.model.license import LicenseDAO


def build_dispensary_map_dict(row):
    result = {'dispensary_id': row[0], 'dispensary_name': row[1], 'dispensary_phone': row[2],
              'dispensary_location': row[3],
              'dispensary_email': row[4], 'dispensary_password': row[5], 'dispensary_active': row[6]}
    return result


def build_dispensary_attr_dict(dispensary_id, dispensary_name, dispensary_phone, dispensary_location, dispensary_email,
                               dispensary_password, license_id, dispensary_active):
    result = {'dispensary_id': dispensary_id, 'dispensary_name': dispensary_name, 'dispensary_phone': dispensary_phone,
              'dispensary_location': dispensary_location, 'dispensary_email': dispensary_email,
              'dispensary_password': dispensary_password, 'license_id': license_id,
              'dispensary_active': dispensary_active}
    return result


class BaseDispensary:

    def createDispensary(self, json):
        dispensary_name = json['dispensary_name']
        dispensary_phone = json['registration_phone']
        dispensary_location = json['dispensary_location']
        dispensary_email = json['registration_email']
        dispensary_password = json['registration_password']
        license_type = json['license_type']
        license_name = json['license_name']
        license_expiration = json['license_expiration']
        license_file = json['license_file']
        dispensary_dao = DispensaryDAO()
        existing_dispensary = dispensary_dao.getDispensaryByEmail(dispensary_email)
        license_dao = LicenseDAO()
        existing_license = license_dao.getLicenseByName(license_name)
        if not existing_dispensary and not existing_license:  # Dispensary with that email and license does not exist
            license_id = license_dao.createLicense(license_type, license_name, license_expiration, license_file)
            dispensary_id = dispensary_dao.createDispensary(dispensary_name, dispensary_phone, dispensary_location,
                                                            dispensary_email, dispensary_password, license_id)
            result = build_dispensary_attr_dict(dispensary_id, dispensary_name, dispensary_phone, dispensary_location,
                                                dispensary_email, dispensary_password, license_id, True)
            return jsonify(result), 201
        else:
            return jsonify("User already exists"), 409

    def getAllDispensaries(self):
        dispensary_dao = DispensaryDAO()
        dispensaries_list = dispensary_dao.getAllDispensaries()
        if not dispensaries_list:  # Dispensary List is empty
            return jsonify("No Dispensaries Found"), 404
        else:
            result_list = []
            for row in dispensaries_list:
                obj = build_dispensary_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list), 200

    def getAllActiveDispensaries(self):
        dispensary_dao = DispensaryDAO()
        dispensaries_list = dispensary_dao.getAllActiveDispensaries()
        if not dispensaries_list:  # Dispensary List is empty
            return jsonify("No Dispensaries Found"), 404
        else:
            result_list = []
            for row in dispensaries_list:
                obj = build_dispensary_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list), 200

    def getDispensaryById(self, dispensary_id):
        dispensary_dao = DispensaryDAO()
        dispensary_tuple = dispensary_dao.getDispensaryById(dispensary_id)
        if not dispensary_tuple:  # Dispensary Not Found
            return jsonify("Dispensary Not Found"), 404
        else:
            result = build_dispensary_map_dict(dispensary_tuple)
        return jsonify(result), 200

    def verifyDispensaryLogin(self, json):
        dispensary_email = json['login_email']
        dispensary_password = json['login_password']
        dispensary_dao = DispensaryDAO()
        valid_dispensary = dispensary_dao.verifyDispensaryLogin(dispensary_email, dispensary_password)
        if not valid_dispensary:
            return jsonify("Username or Password entered incorrectly"), 404
        else:
            return jsonify("Dispensary logged in successfully", valid_dispensary[0],
                           valid_dispensary[4]), 200  # Returns ID & Email
