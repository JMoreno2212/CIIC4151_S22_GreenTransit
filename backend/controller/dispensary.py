import os

from flask import jsonify

from backend.model.dispensary import DispensaryDAO
from backend.model.license import LicenseDAO
from backend.aws_management import AWSHandler


def build_dispensary_map_dict(row):
    result = {'dispensary_id': row[0], 'dispensary_name': row[1], 'dispensary_phone': row[2],
              'dispensary_direction': row[3], 'dispensary_municipality': row[4], 'dispensary_zipcode': row[5],
              'dispensary_email': row[6], 'dispensary_password': row[7], 'license_id': row[8],
              'dispensary_active': row[9], 'dispensary_picture': row[10]}
    return result


def build_dispensary_attr_dict(dispensary_id, dispensary_name, dispensary_phone, dispensary_direction,
                               dispensary_municipality, dispensary_zipcode, dispensary_email,
                               dispensary_password, license_id, dispensary_active, dispensary_picture):
    result = {'dispensary_id': dispensary_id, 'dispensary_name': dispensary_name, 'dispensary_phone': dispensary_phone,
              'dispensary_direction': dispensary_direction, 'dispensary_municipality': dispensary_municipality,
              'dispensary_zipcode': dispensary_zipcode, 'dispensary_email': dispensary_email,
              'dispensary_password': dispensary_password, 'license_id': license_id,
              'dispensary_active': dispensary_active, 'dispensary_picture': dispensary_picture}
    return result


class BaseDispensary:

    def createDispensary(self, json, files):
        dispensary_name = json['dispensary_name']
        dispensary_phone = json['registration_phone']
        dispensary_direction = json['dispensary_direction']
        dispensary_municipality = json['dispensary_municipality']
        dispensary_zipcode = json['dispensary_zipcode']
        dispensary_email = json['registration_email']
        dispensary_password = json['registration_password']
        dispensary_picture = files.get('registration_picture')
        license_type = json['registration_type']
        license_name = json['license_name']
        license_expiration = json['license_expiration']
        license_file = files.get('license_file')
        dispensary_dao = DispensaryDAO()
        existing_dispensary = dispensary_dao.getDispensaryByEmail(dispensary_email)
        license_dao = LicenseDAO()
        existing_license = license_dao.getLicenseByName(license_name)
        if not existing_dispensary and not existing_license:  # Dispensary with that email and license does not exist
            aws_handler = AWSHandler()
            uploaded_license = aws_handler.upload_file(license_name, os.getenv('BUCKET_NAME'))
            uploaded_picture = aws_handler.upload_file(dispensary_picture, os.getenv('BUCKET_NAME'))
            if not uploaded_license or not uploaded_picture:  # Upload failed
                aws_handler.delete_file(license_name, os.getenv('BUCKET_NAME'))
                aws_handler.delete_file(dispensary_picture, os.getenv('BUCKET_NAME'))
                return jsonify("Error reading input files"), 409
            license_id = license_dao.createLicense(license_type, license_name, license_expiration,
                                                   license_file.filename)
            dispensary_id = dispensary_dao.createDispensary(dispensary_name, dispensary_phone, dispensary_direction,
                                                            dispensary_municipality, dispensary_zipcode,
                                                            dispensary_email, dispensary_password, license_id,
                                                            dispensary_picture.filename)
            result = build_dispensary_attr_dict(dispensary_id, dispensary_name, dispensary_phone, dispensary_direction,
                                                dispensary_municipality, dispensary_zipcode, dispensary_email,
                                                dispensary_password, license_id, True, dispensary_picture.filename)
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
            return None
        else:
            return jsonify("Dispensary logged in successfully", valid_dispensary[0],
                           valid_dispensary[6], "Dispensary"), 200  # Returns ID, Email & Type

    def resetPassword(self, json):
        dispensary_dao = DispensaryDAO()
        dispensary_email = json['email']
        new_password = json['password']
        reset_password = dispensary_dao.resetPassword(dispensary_email, new_password)
        if not reset_password:  # No dispensary password was reset
            return None
        else:
            updated_dispensary = dispensary_dao.getDispensaryByEmail(dispensary_email)
            result = build_dispensary_map_dict(updated_dispensary)
            return jsonify(result), 200

    def updateDispensaryData(self, dispensary_id, json):
        dispensary_dao = DispensaryDAO()
        dispensary_name = json['dispensary_name']
        dispensary_phone = json['dispensary_phone']
        dispensary_direction = json['dispensary_direction']
        dispensary_municipality = json['dispensary_municipality']
        dispensary_zipcode = json['dispensary_zipcode']
        dispensary_email = json['dispensary_email']
        dispensary_password = json['dispensary_password']
        new_email = dispensary_dao.getDispensaryByEmail(dispensary_email)
        # New email doesn't exist or is the same as current
        if (not new_email) or (dispensary_email == dispensary_dao.getDispensaryById(dispensary_id)[6]):
            dispensary_dao.updateDispensaryData(dispensary_id, dispensary_name, dispensary_phone, dispensary_direction,
                                                dispensary_municipality, dispensary_zipcode, dispensary_email,
                                                dispensary_password)
            updated_dispensary = dispensary_dao.getDispensaryById(dispensary_id)
            result = build_dispensary_map_dict(updated_dispensary)
            return jsonify(result), 200
        else:
            return jsonify("Email address is already in use"), 409

    def updateDispensaryPicture(self, dispensary_id, files):
        dispensary_dao = DispensaryDAO()
        dispensary_picture = files.get('dispensary_picture')
        aws_handler = AWSHandler()
        uploaded_picture = aws_handler.upload_file(dispensary_picture, os.getenv('BUCKET_NAME'))
        if not uploaded_picture:  # Upload failed
            aws_handler.delete_file(dispensary_picture, os.getenv('BUCKET_NAME'))
            return jsonify("Error reading input files"), 409
        dispensary_dao.updateDispensaryPicture(dispensary_id, dispensary_picture.filename)
        updated_dispensary = dispensary_dao.getDispensaryById(dispensary_id)
        result = build_dispensary_map_dict(updated_dispensary)
        return jsonify(result), 200

    def deleteDispensary(self, dispensary_id):
        dispensary_dao = DispensaryDAO()
        dispensary_dao.deleteDispensary(dispensary_id)
        deleted_dispensary = dispensary_dao.getDispensaryById(dispensary_id)
        deleted_license_id = deleted_dispensary[8]
        license_dao = LicenseDAO()
        license_dao.deleteLicense(deleted_license_id)
        result = build_dispensary_map_dict(deleted_dispensary)
        return jsonify(result), 200
