from flask import jsonify

from backend.model.dispensary import DispensaryDAO
from backend.model.user import UserDAO


class BaseDispensary:
    def build_dispensary_map_dict(self, row):
        result = {'dispensary_id': row[0], 'dispensary_name': row[1], 'dispensary_phone': row[2],
                  'dispensary_location': row[3],
                  'dispensary_email': row[4], 'dispensary_password': row[5], 'dispensary_active': row[6]}
        return result

    def getAllDispensaries(self):
        dispensary_dao = DispensaryDAO()
        dispensaries_list = dispensary_dao.getAllDispensaries()
        if not dispensaries_list:  # Dispensary List is empty
            return jsonify("No Dispensaries Found"), 404
        else:
            result_list = []
            for row in dispensaries_list:
                obj = self.build_dispensary_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list), 200

    def getDispensaryById(self, dispensary_id):
        dao = DispensaryDAO()
        dispensary_tuple = dao.getDispensaryById(dispensary_id)
        if not dispensary_tuple:  # Dispensary Not Found
            return jsonify("Dispensary Not Found"), 404
        else:
            result = self.build_dispensary_map_dict(dispensary_tuple)
        return jsonify(result), 200

