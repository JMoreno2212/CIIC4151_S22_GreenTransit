import os

from flask import jsonify
from backend.controller.license import LicenseDAO
from backend.model.user import UserDAO
from backend.aws_management import AWSHandler


def build_user_map_dict(row):
    result = {'user_id': row[0], 'user_first_name': row[1], 'user_last_name': row[2], 'user_birth_date': row[3],
              'user_phone': row[4], 'user_email': row[5], 'user_password': row[6], 'license_id': row[7],
              'user_active': row[8], 'user_picture': row[9]}
    return result


def build_user_attr_dict(user_id, user_first_name, user_last_name, user_birth_date, user_phone, user_email,
                         user_password, license_id, user_active, user_picture):
    result = {'user_id': user_id, 'user_first_name': user_first_name, 'user_last_name': user_last_name,
              'user_birth_date': user_birth_date, 'user_phone': user_phone, 'user_email': user_email,
              'user_password': user_password, 'license_id': license_id, 'user_active': user_active,
              'user_picture': user_picture}
    return result


class BaseUser:

    def createUser(self, files):
        user_first_name = files['registration_first_name']
        user_last_name = files['registration_last_name']
        user_birth_date = files['registration_birth_date']
        user_phone = files['registration_phone']
        user_email = files['registration_email']
        user_password = files['registration_password']
        license_type = files['registration_type']
        license_name = files['license_name']
        license_expiration = files['license_expiration']
        license_file = files['license_file']
        license_file.save("uploads/" + license_file.filename)
        user_picture = files['registration_picture']
        user_picture.save("uploads/" + user_picture.filename)
        user_dao = UserDAO()
        existing_user = user_dao.getUserByEmail(user_email)
        license_dao = LicenseDAO()
        existing_license = license_dao.getLicenseByName(license_name)
        if not existing_user and not existing_license:  # User with that email and license number does not exist
            aws_handler = AWSHandler()
            license_file_name = 'license_file' + os.getenv('FILE_COUNTER') + '.pdf'
            uploaded_license = aws_handler.upload_file(license_file, os.getenv('BUCKET_NAME'), license_file_name)
            os.environ['FILE_COUNTER'] = str(int(os.getenv('FILE_COUNTER')) + 1)  # Increment File Counter

            user_picture_name = 'user_picture' + os.getenv('FILE_COUNTER') + '.png'
            uploaded_picture = aws_handler.upload_file(user_picture, os.getenv('BUCKET_NAME'), user_picture_name)
            os.environ['FILE_COUNTER'] = str(int(os.getenv('FILE_COUNTER')) + 1)  # Increment File Counter

            if not uploaded_license or not uploaded_picture:  # Upload failed
                aws_handler.delete_file(license_file, os.getenv('BUCKET_NAME'))
                aws_handler.delete_file(user_picture, os.getenv('BUCKET_NAME'))
                os.environ['FILE_COUNTER'] = str(int(os.getenv('FILE_COUNTER')) - 2)  # Decrease File Counter by 2
                return jsonify("Error reading input files"), 409
            license_id = license_dao.createLicense(license_type, license_name, license_expiration,
                                                   license_file_name)
            user_id = user_dao.createUser(user_first_name, user_last_name, user_birth_date, user_phone, user_email,
                                          user_password, license_id, user_picture_name)
            result = build_user_attr_dict(user_id, user_first_name, user_last_name, user_birth_date, user_phone,
                                          user_email, user_password, license_id, True, user_picture_name)
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

    def resetPassword(self, json):
        user_dao = UserDAO()
        user_email = json['email']
        new_password = json['password']
        reset_password = user_dao.resetPassword(user_email, new_password)
        if not reset_password:  # No user password was reset
            return None
        else:
            updated_user = user_dao.getUserByEmail(user_email)
            result = build_user_map_dict(updated_user)
            return jsonify(result), 200

    def updateUserData(self, user_id, json):
        user_dao = UserDAO()
        user_phone = json['user_phone']
        user_email = json['user_email']
        user_password = json['user_password']
        new_email = user_dao.getUserByEmail(user_email)
        # New email doesn't exist or is the same as current
        if (not new_email) or (user_email == user_dao.getUserById(user_id)[5]):
            user_dao.updateUserData(user_id, user_phone, user_email, user_password)
            updated_user = user_dao.getUserById(user_id)
            result = build_user_map_dict(updated_user)
            return jsonify(result), 200
        else:
            return jsonify("Email address is already in use"), 409

    def updateUserPicture(self, user_id, files):
        user_dao = UserDAO()
        user_picture = files['user_picture']
        aws_handler = AWSHandler()
        user_picture.save("uploads/" + user_picture.filename)
        object_name = 'user_picture' + os.getenv('FILE_COUNTER') + '.pdf'
        uploaded_picture = aws_handler.upload_file(user_picture, os.getenv('BUCKET_NAME'), object_name)
        if not uploaded_picture:  # Upload failed
            return jsonify("Error reading input files"), 409
        os.environ['FILE_COUNTER'] = str(int(os.getenv('FILE_COUNTER')) + 1)  # Increment File Counter
        user_dao.updateUserPicture(user_id, object_name)
        updated_user = user_dao.getUserById(user_id)
        result = build_user_map_dict(updated_user)
        return jsonify(result), 200

    def verifyUserLogin(self, json):
        user_email = json['login_email']
        user_password = json['login_password']
        user_dao = UserDAO()
        valid_user = user_dao.verifyUserLogin(user_email, user_password)
        if not valid_user:
            return None
        else:
            # Returns ID, Email & Type
            return jsonify("User logged in successfully", valid_user[0], valid_user[5], "User"), 200
