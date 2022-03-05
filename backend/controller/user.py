from flask import jsonify

from backend.model.user import UserDAO


def build_user_map_dict(row):
    result = {'user_id': row[0], 'user_first_name': row[1], 'user_last_name': row[2], 'user_birth_date': row[3],
              'user_phone': row[4], 'user_email': row[5], 'user_password': row[6], 'license_id': row[7],
              'user_Active': row[8]}
    return result


class BaseUser:

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

    def getUserById(self, user_id):
        user_dao = UserDAO()
        user_tuple = user_dao.getUserById(user_id)
        if not user_tuple: # User Not Found
            return jsonify("User Not Found"), 404
        else:
            result = build_user_map_dict(user_tuple)
            return jsonify(result), 200
