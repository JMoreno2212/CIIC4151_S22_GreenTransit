from flask import jsonify

from backend.controller.license import LicenseDAO
from backend.model.user import UserDAO


def build_user_map_dict(row):
    result = {'user_id': row[0], 'user_first_name': row[1], 'user_last_name': row[2], 'user_birth_date': row[3],
              'user_phone': row[4], 'user_email': row[5], 'user_password': row[6], 'license_id': row[7],
              'user_active': row[8]}
    return result


def build_user_attr_dict(user_id, user_first_name, user_last_name, user_birth_date, user_phone, user_email,
                         user_password, license_id, user_active):
    result = {'user_id': user_id, 'user_first_name': user_first_name, 'user_last_name': user_last_name,
              'user_birth_date': user_birth_date, 'user_phone': user_phone, 'user_email': user_email,
              'user_password': user_password, 'license_id': license_id, 'user_active': user_active}
    return result


class BaseUser:

    def createUser(self, json):
        user_first_name = json['registration_first_name']
        user_last_name = json['registration_last_name']
        user_birth_date = json['registration_birth_date']
        user_phone = json['registration_phone']
        user_email = json['registration_email']
        user_password = json['registration_password']
        license_type = json['registration_type']
        license_name = json['license_name']
        license_expiration = json['license_expiration']
        license_file = json['license_file']
        user_dao = UserDAO()
        existing_user = user_dao.getUserByEmail(user_email)
        license_dao = LicenseDAO()
        existing_license = license_dao.getLicenseByName(license_name)
        if not existing_user and not existing_license:  # User with that email and license number does not exist
            license_id = license_dao.createLicense(license_type, license_name, license_expiration, license_file)
            user_id = user_dao.createUser(user_first_name, user_last_name, user_birth_date, user_phone, user_email,
                                          user_password, license_id)
            result = build_user_attr_dict(user_id, user_first_name, user_last_name, user_birth_date, user_phone,
                                          user_email, user_password, license_id, True)
            return jsonify(result), 201
        else:
            return jsonify("User already exists"), 409

    def deleteUser(self, user_id):
        user_dao = UserDAO()
        user_dao.deleteUser(user_id)
        deleted_user = user_dao.getUserById(user_id)
        deleted_license_id = deleted_user[7]
        license_dao = LicenseDAO()
        license_dao.deleteLicense(deleted_license_id)
        result = build_user_map_dict(deleted_user)
        return jsonify(result), 200

    def getAllUsers(self):
        user_dao = UserDAO()
        users_list = user_dao.getAllUsers()
        if not users_list:  # User List is empty
            return jsonify("No Users Found"), 404
        else:
            result_list = []
            for row in users_list:
                obj = build_user_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list), 200

    def getAllActiveUsers(self):
        user_dao = UserDAO()
        users_list = user_dao.getAllActiveUsers()
        if not users_list:  # User List is empty
            return jsonify("No Users Found"), 404
        else:
            result_list = []
            for row in users_list:
                obj = build_user_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list), 200

    def getUserById(self, user_id):
        user_dao = UserDAO()
        user_tuple = user_dao.getUserById(user_id)
        if not user_tuple:  # User Not Found
            return jsonify("User Not Found"), 404
        else:
            result = build_user_map_dict(user_tuple)
            return jsonify(result), 200

    def updateUser(self, user_id, json):
        user_dao = UserDAO()
        user_phone = json['user_phone']
        user_email = json['user_email']
        user_password = json['user_password']
        existing_email = user_dao.getUserByEmail(user_email)
        if not existing_email:
            updated_user = user_dao.updateUser(user_id, user_phone, user_email, user_password)
            result = build_user_map_dict(updated_user)
            return jsonify(result), 200
        else:
            return jsonify("Email address is already in use"), 409

    def verifyUserLogin(self, json):
        user_email = json['login_email']
        user_password = json['login_password']
        user_dao = UserDAO()
        valid_user = user_dao.verifyUserLogin(user_email, user_password)
        if not valid_user:
            return None
        else:
            return jsonify("User logged in successfully", valid_user[0], valid_user[5]), 200  # Returns ID & Email
