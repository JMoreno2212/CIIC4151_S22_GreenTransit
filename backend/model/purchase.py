import os

import psycopg2


class PurchaseDAO:
    def __init__(self):
        self.conn = psycopg2.connect(os.getenv('DATABASE_URL'))

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

    def getPurchaseById(self, purchase_id):
        cursor = self.conn.cursor()
        query = 'select * from "Purchase" where purchase_id = %s'
        cursor.execute(query, (purchase_id,))
        result = cursor.fetchone()
        cursor.close()
        return result
