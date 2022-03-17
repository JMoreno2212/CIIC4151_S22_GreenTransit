import os

from flask import jsonify
from cryptography.fernet import Fernet
from backend.model.license import LicenseDAO


def build_license_map_dict(row):
    # fernet = Fernet(os.getenv('LICENSE_KEY'))
    result = {'license_id': row[0], 'license_type': row[1], 'license_name': row[2], 'license_expiration': row[3],
              'license_file': row[4], 'license_active': row[5]}
    # print(result)
    return result


def build_license_attr_dict(license_id, license_type, license_name, license_expiration, license_file, license_active):
    # fernet = Fernet(os.getenv('LICENSE_KEY'))
    result = {'license_id': license_id, 'license_type': license_type, 'license_name': license_name,
              'license_expiration': license_expiration, 'license_file': license_file, 'license_active': license_active}
    return result


class BaseLicense:

    # def createLicense(self, json):  # THIS ONE WILL NOT HAVE AN ENDPOINT SINCE IT DOES NOT MAKE SENSE
    #     license_type = json['registration_type']
    #     license_name = json['license_name']
    #     license_expiration = json['license_expiration']
    #     license_file = json['license_file']
    #     license_dao = LicenseDAO()
    #     existing_license = license_dao.getLicenseByName(license_name)
    #     if not existing_license:  # License is not already in use
    #         license_id = license_dao.createLicense(license_type, license_name, license_expiration, license_file)
    #         result = build_license_attr_dict(license_id, license_type, license_name, license_expiration, license_file,
    #                                          True)
    #         return result
    #     else:
    #         return None

    def getAllLicenses(self):
        license_dao = LicenseDAO()
        licenses_list = license_dao.getAllLicenses()
        if not licenses_list:  # Licenses List is empty
            return jsonify("No Licenses Found"), 404
        else:
            result_list = []
            for row in licenses_list:
                obj = build_license_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list), 200

    def getAllActiveLicenses(self):
        license_dao = LicenseDAO()
        licenses_list = license_dao.getAllActiveLicenses()
        if not licenses_list:  # Licenses List is empty
            return jsonify("No Licenses Found"), 404
        else:
            result_list = []
            for row in licenses_list:
                obj = build_license_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list), 200

    def getLicensesById(self, license_id):
        license_dao = LicenseDAO()
        license_tuple = license_dao.getLicenseById(license_id)
        if not license_tuple:  # License Not Found
            return jsonify("License Not Found"), 404
        else:
            result = build_license_map_dict(license_tuple)
            return jsonify(result), 200
