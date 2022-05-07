from flask import jsonify

from backend.model.dispensary import DispensaryDAO
from backend.model.item import ItemDAO


def build_item_map_dict(row):
    result = {'item_id': row[0], 'item_name': row[1], 'item_description': row[2], 'item_quantity': row[3],
              'item_price': row[4], 'item_category': row[5], 'item_type': row[6], 'dispensary_id': row[7],
              'item_active': row[8], 'item_picture': row[9]}
    return result


def build_item_attr_dict(item_id, item_name, item_description, item_quantity, item_price, item_category, item_type,
                         dispensary_id, item_active, item_picture):
    result = {'item_id': item_id, 'item_name': item_name, 'item_description': item_description,
              'item_quantity': item_quantity, 'item_price': item_price, 'item_category': item_category,
              'item_type': item_type, 'dispensary_id': dispensary_id, 'item_active': item_active,
              'item_picture': item_picture}
    return result


class BaseItem:

    def createItem(self, dispensary_id, json):
        item_name = json['item_name']
        item_description = json['item_description']
        item_quantity = json['item_quantity']
        item_price = json['item_price']
        item_category = json['item_category']
        item_type = json['item_type']
        item_picture = json['item_picture']
        item_dao = ItemDAO()
        item_id = item_dao.createItem(item_name, item_description, item_quantity, item_price, item_category, item_type,
                                      dispensary_id, item_picture)
        result = build_item_attr_dict(item_id, item_name, item_description, item_quantity, item_price, item_category,
                                      item_type, dispensary_id, True, item_picture)
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

    def updateItemData(self, dispensary_id, item_id, json):
        item_dao = ItemDAO()
        item_name = json['item_name']
        item_description = json['item_description']
        item_price = json['item_price']
        item_category = json['item_category']
        item_type = json['item_type']
        item_dao.updateItemData(dispensary_id, item_id, item_name, item_description, item_price, item_category,
                                item_type)
        updated_item = item_dao.getItemById(item_id)
        result = build_item_map_dict(updated_item)
        return jsonify(result), 200

    def updateItemPicture(self, item_id, json):
        item_dao = ItemDAO()
        item_picture = json['item_picture']
        item_dao.updateItemPicture(item_id, item_picture)
        updated_item = item_dao.getItemById(item_id)
        result = build_item_map_dict(updated_item)
        return jsonify(result), 200

    def deleteItemAtDispensary(self, dispensary_id, item_id):
        item_dao = ItemDAO()
        item_dao.deleteItemAtDispensary(dispensary_id, item_id)
        deleted_item = item_dao.getDeletedItemById(item_id)
        result = build_item_map_dict(deleted_item)
        return jsonify(result), 200

    def getItemByCategory(self, item_category):
        item_dao = ItemDAO()
        item_tuple = item_dao.getItemByCategory(item_category)
        if not item_tuple:  # Item Not Found
            return jsonify("Item Not Found"), 404
        else:
            result = build_item_map_dict(item_tuple)
        return jsonify(result), 200

    def getItemByFilter(self, item_filter):
        item_dao = ItemDAO()
        item_filter_name = item_filter
        item_filter_description = item_filter
        item_filter_category = item_filter
        item_filter_type = item_filter
        item_tuple = item_dao.getItemByFilter(item_filter_name, item_filter_description, item_filter_category,
                                              item_filter_type)
        if not item_tuple:  # Item Not Found
            return jsonify("Item Not Found"), 404
        else:
            result = build_item_map_dict(item_tuple)
        return jsonify(result), 200

    def getItemByPriceRange(self, json):
        item_dao = ItemDAO()
        item_price_top = json['item_price_top']
        item_price_bottom = json['item_price_bottom']
        item_tuple = item_dao.getItemByPriceRange(item_price_bottom, item_price_top)
        if not item_tuple:  # Item Not Found
            return jsonify("Item Not Found"), 404
        else:
            result = build_item_map_dict(item_tuple)
        return jsonify(result), 200
