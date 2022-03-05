from flask import jsonify

from backend.model.purchase import PurchaseDAO


def build_purchase_map_dict(row):
    result = {'purchase_id': row[0], 'user_id': row[1], 'dispensary_id': row[2], 'purchase_date': row[3],
              'purchase_total': row[4], 'item_id': row[5], 'purchase_item_quantity': row[6]}
    return result


class BasePurchase:

    def getAllPurchases(self):
        purchase_dao = PurchaseDAO()
        purchases_list = purchase_dao.getAllPurchases()
        if not purchases_list: # Purchase List is empty
            return jsonify("No Purchases Found"), 404
        else:
            result_list = []
            for row in purchases_list:
                obj = build_purchase_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list), 200

    def getPurchaseById(self, purchase_id):
        purchase_dao = PurchaseDAO()
        purchase_tuple = purchase_dao.getPurchaseById(purchase_id)
        if not purchase_tuple:  # Purchase Not Found
            return jsonify("Purchase Not Found"), 404
        else:
            result = build_purchase_map_dict(purchase_tuple)
            return jsonify(result), 200
