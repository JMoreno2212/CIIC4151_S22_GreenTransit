from flask import jsonify

from backend.model.dispensary import DispensaryDAO
from backend.model.item import ItemDAO


def build_item_map_dict(row):
    result = {'item_id': row[0], 'item_name': row[1], 'item_description': row[2], 'item_quantity': row[3],
              'item_price': row[4], 'item_category': row[5], 'item_type': row[6], 'dispensary_id': row[7],
              'item_active': row[8]}
    return result


def build_item_attr_dict(item_id, item_name, item_description, item_quantity, item_price, item_category, item_type,
                         dispensary_id, item_active):
    result = {'item_id': item_id, 'item_name': item_name, 'item_description': item_description,
              'item_quantity': item_quantity, 'item_price': item_price, 'item_category': item_category,
              'item_type': item_type, 'dispensary_id': dispensary_id, 'item_active': item_active}
    return result


class BaseItem:

    def createItem(self, dispensary_id, json):
        item_name = json['item_name']
        item_description = json['item_description']
        item_quantity = json['item_quantity']
        item_price = json['item_price']
        item_category = json['item_category']
        item_type = json['item_type']
        item_dao = ItemDAO()
        item_id = item_dao.createItem(item_name, item_description, item_quantity, item_price, item_category, item_type,
                                      dispensary_id)
        result = build_item_attr_dict(item_id, item_name, item_description, item_quantity, item_price, item_category,
                                      item_type, dispensary_id, True)
        return jsonify(result), 200

    def getAllItems(self):
        item_dao = ItemDAO()
        items_list = item_dao.getAllItems()
        if not items_list:  # Item List is empty
            return jsonify("No Items Found"), 404
        else:
            result_list = []
            for row in items_list:
                obj = build_item_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list), 200

    def getAllActiveItems(self):
        item_dao = ItemDAO()
        items_list = item_dao.getAllActiveItems()
        if not items_list:  # Item List is empty
            return jsonify("No Items Found"), 404
        else:
            result_list = []
            for row in items_list:
                obj = build_item_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list), 200

    def getItemById(self, item_id):
        item_dao = ItemDAO()
        item_tuple = item_dao.getItemById(item_id)
        if not item_tuple:  # Item Not Found
            return jsonify("Item Not Found"), 404
        else:
            result = build_item_map_dict(item_tuple)
        return jsonify(result), 200

    def getAllItemsAtDispensary(self, dispensary_id):
        dispensary_dao = DispensaryDAO()
        valid_dispensary = dispensary_dao.getDispensaryById(dispensary_id)
        if not valid_dispensary:
            return jsonify("Dispensary Not Found"), 404
        item_dao = ItemDAO()
        items_list = item_dao.getAllItemsAtDispensary(dispensary_id)
        if not items_list:
            return jsonify("No Items Found"), 404
        else:
            result_list = []
            for row in items_list:
                obj = build_item_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list), 200

    def getItemAtDispensary(self, dispensary_id, item_id):
        dispensary_dao = DispensaryDAO()
        valid_dispensary = dispensary_dao.getDispensaryById(dispensary_id)
        if not valid_dispensary:
            return jsonify("Dispensary Not Found"), 404
        item_dao = ItemDAO()
        item_tuple = item_dao.getItemAtDispensary(dispensary_id, item_id)
        if not item_tuple:  # Item Not Found
            return jsonify("Item Not Found"), 404
        else:
            result = build_item_map_dict(item_tuple)
        return jsonify(result), 200
