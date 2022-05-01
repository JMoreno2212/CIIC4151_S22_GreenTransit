import os

import psycopg2


class PurchaseDAO:
    def __init__(self):
        self.conn = psycopg2.connect(os.getenv('DATABASE_URL'))

    # ----------------------------------------------------------------------------------------------------------------
    #                                                     Create                                                     #
    # ----------------------------------------------------------------------------------------------------------------
    def createPurchase(self, user_id, dispensary_id, purchase_number, purchase_type, purchase_date, purchase_total):
        cursor = self.conn.cursor()
        query = 'insert into "Purchase" (user_id, dispensary_id, purchase_number, purchase_type, purchase_date, ' \
                'purchase_total) values (%s, %s, %s, %s, %s, %s) returning purchase_id'
        cursor.execute(query, (user_id, dispensary_id, purchase_number, purchase_type, purchase_date, purchase_total))
        purchase_id = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        return purchase_id

    def createPurchasedItem(self, purchase_id, item_id, purchased_quantity, item_subtotal):
        cursor = self.conn.cursor()
        query = 'insert into "PurchasedItems" (purchase_id, item_id, purchased_quantity, item_subtotal) ' \
                'values (%s, %s, %s, %s)'
        cursor.execute(query, (purchase_id, item_id, purchased_quantity, item_subtotal))
        self.conn.commit()
        cursor.close()
        return cursor.rowcount != 0

    # ----------------------------------------------------------------------------------------------------------------
    #                                                      Read                                                      #
    # ----------------------------------------------------------------------------------------------------------------
    def getAllPurchases(self):
        cursor = self.conn.cursor()
        query = 'select * from "Purchase";'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def getAllPurchasesAtDispensary(self, dispensary_id):
        cursor = self.conn.cursor()
        query = 'select * from "Purchase" where dispensary_id = %s;'
        cursor.execute(query, (dispensary_id,))
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def getPurchaseById(self, purchase_id):
        cursor = self.conn.cursor()
        query = 'select * from "Purchase" where purchase_id = %s'
        cursor.execute(query, (purchase_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def getPurchaseByIdAtDispensary(self, dispensary_id, purchase_id):
        cursor = self.conn.cursor()
        query = 'select * from "Purchase" where dispensary_id = %s and purchase_id = %s'
        cursor.execute(query, (dispensary_id, purchase_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def getPurchasesByUser(self, user_id):
        cursor = self.conn.cursor()
        query = 'select * from "Purchase" where user_id = %s'
        cursor.execute(query, (user_id,))
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    # ----------------------------------------------------------------------------------------------------------------
    #                                                     Update                                                     #
    # ----------------------------------------------------------------------------------------------------------------
    def updatePurchase(self, purchase_id, purchase_type, purchase_total):
        cursor = self.conn.cursor()
        query = 'update "Purchase" set purchase_type = %s, purchase_total = %s where purchase_id = %s'
        cursor.execute(query, (purchase_type, purchase_total, purchase_id,))
        self.conn.commit()
        cursor.close()
        return cursor.rowcount != 0
