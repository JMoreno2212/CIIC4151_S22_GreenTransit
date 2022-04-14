from flask import jsonify

from backend.model.purchase import PurchaseDAO


def build_purchase_map_dict(row):
    result = {'purchase_id': row[0], 'user_id': row[1], 'dispensary_id': row[2], 'purchase_number': row[3],
              'purchase_type': row[4], 'purchase_date': row[5], 'purchase_total': row[6]}
    return result

def build_purchase_attr_dict(purchase_id, user_id, dispensary_id, purchase_number, purchase_type, purchase_date, purchase_total):
    result = {'purchase_id': purchase_id, 'user_id': user_id, 'dispensary_id': dispensary_id, 'purchase_number': purchase_number,
              'purchase_type': purchase_type, 'purchase_date': purchase_date, 'purchase_total': purchase_total}
    return result

class BasePurchase:

    def createPurchase(self, user_id, dispensary_id, json):
        purchase_number = json['purchase_number']
        purchase_type = json['purchase_type']
        purchase_date = json['purchase_date']
        purchase_total = json['purchase_total']
        purchase_dao = PurchaseDAO()
        purchase_id = purchase_dao.createPurchase(user_id, dispensary_id, purchase_number, purchase_type, purchase_date,
                                                  purchase_total)
        result = build_purchase_attr_dict(purchase_id, user_id, dispensary_id, purchase_number, purchase_type, purchase_date,
                                          purchase_total)
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

    def getPurchaseById(self, purchase_id):
        purchase_dao = PurchaseDAO()
        purchase_tuple = purchase_dao.getPurchaseById(purchase_id)
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

    def updatePurchase(self, purchase_id, json):
        purchase_dao = PurchaseDAO()
        purchase_id = json['purchase_id']
        dispensary_id = json['dispensary_id']
        purchase_number = json['purchase_number']
        purchase_type = json['purchase_type']
        purchase_date = json['purchase_date']
        purchase_total = json['purchase_total']
        new_email = user_dao.getUserByEmail(user_email)
        # New email doesn't exist or is the same as current
        if (not new_email) or (user_email == user_dao.getUserById(user_id)[5]):
            purchase_dao.updatePurchase(user_id, user_phone, user_email, user_password)
            updated_user = user_dao.getUserById(user_id)
            result = build_user_map_dict(updated_user)
            return jsonify(result), 200
        else:
            return jsonify("Email address is already in use"), 409
