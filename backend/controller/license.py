from flask import jsonify

from backend.model.license import LicenseDAO


def build_license_map_dict(row):
    result = {'license_id': row[0], 'license_type': row[1], 'license_name': row[2], 'license_expiration': row[3],
              'license_file': row[4], 'license_active': row[5]}
    return result


class BaseLicense:

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

    def getLicensesById(self, license_id):
        license_dao = LicenseDAO()
        license_tuple = license_dao.getLicenseById(license_id)
        if not license_tuple:  # License Not Found
            return jsonify("License Not Found"), 404
        else:
            result = build_license_map_dict(license_tuple)
            return jsonify(result), 200
