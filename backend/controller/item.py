from flask import jsonify

from backend.model.dispensary import DispensaryDAO
from backend.model.item import ItemDAO
from backend.model.user import UserDAO




class BaseItem:

    def build_item_map_dict(self, row):
        result = {'item_id': row[0], 'item_name': row[1], 'item_description': row[2], 'item_quantity': row[3],
                  'item_price': row[4], 'dispensary_id': row[5], 'item_active': row[6]}
        return result

    def getAllItems(self):
        item_dao = ItemDAO()
        items_list = item_dao.getAllItems()
        if not items_list:  # Item List is empty
            return jsonify("No Items Found"), 404
        else:
            result_list = []
            for row in items_list:
                obj = self.build_item_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list), 200

    def getItemById(self, item_id):
        dao = ItemDAO()
        item_tuple = dao.getItemById(item_id)
        if not item_tuple:  # Item Not Found
            return jsonify("Item Not Found"), 404
        else:
            result = self.build_item_map_dict(item_tuple)
        return jsonify(result), 200
