from flask import jsonify

from backend.model.dispensary import DispensaryDAO
from backend.model.item import ItemDAO
from backend.model.purchase import PurchaseDAO


def build_purchase_map_dict(row):
    result = {'purchase_id': row[0], 'user_id': row[1], 'dispensary_id': row[2], 'purchase_number': row[3],
              'purchase_type': row[4], 'purchase_date': row[5], 'purchase_total': row[6], 'purchase_completed': row[7]}
    return result


def build_purchase_map_dict_full_info(row):
    result = {'purchase_id': row[0], 'purchase_number': row[1], 'purchase_type': row[2], 'purchase_date': row[3],
              'purchase_total': row[4], 'purchase_completed': row[5], 'purchased_quantity': row[6], 'item_id': row[7],
              'item_name': row[8], 'item_subtotal': row[9], 'item_description': row[10], 'user_id': row[11],
              'user_first_name': row[12], 'user_last_name': row[13], 'user_phone': row[14], 'user_email': row[15]}
    return result


def build_purchase_attr_dict(purchase_id, user_id, dispensary_id, purchase_number, purchase_type, purchase_date,
                             purchase_total, purchase_completed):
    result = {'purchase_id': purchase_id, 'user_id': user_id, 'dispensary_id': dispensary_id,
              'purchase_number': purchase_number,
              'purchase_type': purchase_type, 'purchase_date': purchase_date, 'purchase_total': purchase_total,
              'purchase_completed': purchase_completed}
    return result


class BasePurchase:

    def createPurchase(self, user_id, json):
        dispensary_id = json['dispensary_id']
        purchase_number = json['purchase_number']
        purchase_type = json['purchase_type']
        purchase_date = json['purchase_date']
        purchase_total = json['purchase_total']
        purchased_items = json['purchased_items']  # Tuple with (item_id, purchased_quantity)
        purchase_dao = PurchaseDAO()
        item_dao = ItemDAO()

        # Verify all items have enough quantity
        for item in purchased_items:
            item_id = item[0]
            purchased_quantity = item[1]
            old_quantity = item_dao.getItemQuantityById(item_id)
            new_quantity = old_quantity - purchased_quantity
            if new_quantity < 0:
                return jsonify("Not enough items available"), 409

        # After all items have enough available
        purchase_id = purchase_dao.createPurchase(user_id, dispensary_id, purchase_number, purchase_type, purchase_date,
                                                  purchase_total)

        # Purchase the items and reduce quantities
        for item in purchased_items:
            item_id = item[0]
            purchased_quantity = item[1]
            old_quantity = item_dao.getItemQuantityById(item_id)
            new_quantity = old_quantity - purchased_quantity
            item_price = item_dao.getItemPriceById(item_id)
            item_subtotal = item_price * purchased_quantity
            purchase_dao.createPurchasedItem(purchase_id, item_id, purchased_quantity, item_subtotal)
            item_dao.updateItemQuantity(item_id, new_quantity)

        result = build_purchase_attr_dict(purchase_id, user_id, dispensary_id, purchase_number, purchase_type,
                                          purchase_date, purchase_total, False)
        return jsonify(result), 200

    def getAllPurchases(self):
        purchase_dao = PurchaseDAO()
        purchases_list = purchase_dao.getAllPurchases()
        if not purchases_list:  # Purchase List is empty
            return jsonify("No Purchases Found"), 404
        else:
            result_list = []
            for row in purchases_list:
                obj = build_purchase_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list), 200

    def getAllPurchasesAtDispensary(self, dispensary_id):
        purchase_dao = PurchaseDAO()
        purchases_list = purchase_dao.getAllPurchasesAtDispensary(dispensary_id)
        if not purchases_list:  # Purchase List is empty
            return jsonify("No Purchases Found"), 404
        else:
            result_list = []
            for row in purchases_list:
                obj = build_purchase_map_dict_full_info(row)
                result_list.append(obj)
            return jsonify(result_list), 200

    def getMostSoldItemAtDispensary(self, dispensary_id):
        dispensary_dao = DispensaryDAO()
        valid_dispensary = dispensary_dao.getDispensaryById(dispensary_id)
        if not valid_dispensary:
            return jsonify("Dispensary Not Found"), 404
        purchase_dao = PurchaseDAO()
        most_sold_item = purchase_dao.getMostSoldItemAtDispensary(dispensary_id)
        if not most_sold_item:  # Item Not Found
            return jsonify("Item Not Found"), 404
        else:
            result = most_sold_item[0]
        return jsonify(result), 200

    def getLeastSoldItemAtDispensary(self, dispensary_id):
        dispensary_dao = DispensaryDAO()
        valid_dispensary = dispensary_dao.getDispensaryById(dispensary_id)
        if not valid_dispensary:
            return jsonify("Dispensary Not Found"), 404
        purchase_dao = PurchaseDAO()
        most_sold_item = purchase_dao.getLeastSoldItemAtDispensary(dispensary_id)
        if not most_sold_item:  # Item Not Found
            return jsonify("Item Not Found"), 404
        else:
            result = most_sold_item[0]
        return jsonify(result), 200

    def getTotalOfPurchasesByDispensary(self, dispensary_id):
        purchase_dao = PurchaseDAO()
        purchases_list = purchase_dao.getAllPurchasesAtDispensary(dispensary_id)
        if not purchases_list:  # Purchase List is empty
            return jsonify("No Purchases Found"), 404
        else:
            return jsonify(len(purchases_list)), 200

    def getPurchaseById(self, purchase_id):
        purchase_dao = PurchaseDAO()
        purchase_tuple = purchase_dao.getPurchaseById(purchase_id)
        if not purchase_tuple:  # Purchase Not Found
            return jsonify("Purchase Not Found"), 404
        else:
            result = build_purchase_map_dict(purchase_tuple)
            return jsonify(result), 200

    def getPurchaseByIdAtDispensary(self, dispensary_id, purchase_id):
        purchase_dao = PurchaseDAO()
        purchase_tuple = purchase_dao.getPurchaseByIdAtDispensary(dispensary_id, purchase_id)
        if not purchase_tuple:  # Purchase Not Found
            return jsonify("Purchase Not Found"), 404
        else:
            result = build_purchase_map_dict(purchase_tuple)
            return jsonify(result), 200

    def getPurchasesByUser(self, user_id):
        purchase_dao = PurchaseDAO()
        purchases_list = purchase_dao.getPurchasesByUser(user_id)
        if not purchases_list:
            return jsonify("No Purchases Found"), 404
        else:
            result_list = []
            for row in purchases_list:
                obj = build_purchase_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list), 200

    def getPastPurchasesByUser(self, user_id):
        purchase_dao = PurchaseDAO()
        purchases_list = purchase_dao.getPastPurchasesByUser(user_id)
        if not purchases_list:
            return jsonify("No Purchases Found"), 404
        else:
            result_list = []
            for row in purchases_list:
                obj = build_purchase_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list), 200

    def updatePurchase(self, purchase_id, json):
        purchase_dao = PurchaseDAO()
        purchase_type = json['purchase_type']
        purchase_total = json['purchase_total']
        purchase_dao.updatePurchase(purchase_id, purchase_type, purchase_total)
        updated_purchase = purchase_dao.getPurchaseById(purchase_id)
        result = build_purchase_map_dict(updated_purchase)
        return jsonify(result), 200

    def markPurchaseAsCompleted(self, purchase_id):
        purchase_dao = PurchaseDAO()
        purchase_dao.markPurchaseAsCompleted(purchase_id)
        updated_purchase = purchase_dao.getPurchaseById(purchase_id)
        result = build_purchase_map_dict(updated_purchase)
        return jsonify(result), 200
