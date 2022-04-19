import os

import psycopg2


class DeliveryDAO:
    def __init__(self):
        self.conn = psycopg2.connect(os.getenv('DATABASE_URL'))

    # ----------------------------------------------------------------------------------------------------------------
    #                                                     Create                                                     #
    # ----------------------------------------------------------------------------------------------------------------
    def createDelivery(self, delivery_date, delivery_price, delivery_direction, delivery_municipality, delivery_zipcode,
                       driver_id, vehicle_id, purchase_id):
        cursor = self.conn.cursor()
        query = 'insert into "Delivery" (delivery_date, delivery_price, delivery_direction, delivery_municipality,' \
                'delivery_zipcode, driver_id, vehicle_id, purchase_id) values (%s, %s, %s, %s, %s, %s, %s, %s)' \
                'returning delivery_id'
        cursor.execute(query, (delivery_date, delivery_price, delivery_direction, delivery_municipality,
                               delivery_zipcode, driver_id, vehicle_id, purchase_id))
        delivery_id = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        return delivery_id

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

    # ----------------------------------------------------------------------------------------------------------------
    #                                                     Update                                                     #
    # ----------------------------------------------------------------------------------------------------------------
    # REQUIRES ALL FIELDS TO BE FILLED
    def updateDeliveryInformation(self, delivery_id, delivery_date, delivery_direction, delivery_municipality,
                                  delivery_zipcode):
        cursor = self.conn.cursor()
        query = 'update "Delivery" set delivery_date = %s, delivery_direction = %s, delivery_municipality = %s,' \
                'delivery_zipcode = %s where delivery_id = %s'
        cursor.execute(query, (delivery_date, delivery_direction, delivery_municipality, delivery_zipcode, delivery_id))
        self.conn.commit()
        cursor.close()
        return cursor.rowcount != 0

    def updateDeliveryStatus(self, delivery_id, delivery_status):
        cursor = self.conn.cursor()
        query = 'update "Delivery" set delivery_status = %s where delivery_id = %s'
        cursor.execute(query, (delivery_status, delivery_id))
        self.conn.commit()
        cursor.close()
        return cursor.rowcount != 0
