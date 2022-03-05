import os

import psycopg2


class DeliveryDAO:
    def __init__(self):
        self.conn = psycopg2.connect(os.getenv('DATABASE_URL'))

    # ----------------------------------------------------------------------------------------------------------------
    #                                                      Read                                                      #
    # ----------------------------------------------------------------------------------------------------------------
    def getAllDeliveries(self):
        cursor = self.conn.cursor()
        query = 'select * from "Delivery";'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def getDeliveryById(self, delivery_id):
        cursor = self.conn.cursor()
        query = 'select * from "Delivery" where delivery_id = %s'
        cursor.execute(query, (delivery_id,))
        result = cursor.fetchone()
        cursor.close()
        return result
