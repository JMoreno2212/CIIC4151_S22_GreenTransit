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

    def getAllDeliveriesBasicInfo(self):
        cursor = self.conn.cursor()
        query = 'select delivery_id, delivery_date, delivery_price, delivery_direction, delivery_municipality,' \
                'delivery_zipcode, delivery_status, driver_id, vehicle_id, purchase_id ' \
                'from "Delivery" '
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def getAllDeliveriesFullInfo(self):
        cursor = self.conn.cursor()
        query = 'select delivery_id, driver_id, "Purchase".purchase_id, purchase_number, purchase_date,' \
                '"User".user_id, user_first_name, user_last_name, user_phone, user_email, delivery_direction,' \
                'delivery_municipality, "Dispensary".dispensary_id, dispensary_name, dispensary_phone,' \
                'dispensary_email, dispensary_direction, dispensary_municipality from "User" inner join "Purchase" ' \
                'on "User".user_id = "Purchase".user_id inner join "Delivery" on ' \
                '"Purchase".purchase_id = "Delivery".purchase_id inner join "Dispensary" on ' \
                '"Purchase".dispensary_id = "Dispensary".dispensary_id order by purchase_date;'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def getAllDeliveriesWithoutDriver(self):
        cursor = self.conn.cursor()
        query = 'select delivery_id, delivery_date, delivery_price, delivery_direction, delivery_municipality,' \
                'delivery_zipcode, delivery_status, driver_id, vehicle_id, purchase_id ' \
                'from "Delivery" where driver_id is null;'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def getDeliveryByIdBasicInfo(self, delivery_id):
        cursor = self.conn.cursor()
        query = 'select * from "Delivery" where delivery_id = %s'
        cursor.execute(query, (delivery_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def getDeliveryByIdFullInfo(self, delivery_id):
        cursor = self.conn.cursor()
        query = 'select delivery_id, driver_id, "Purchase".purchase_id, purchase_number, purchase_date,' \
                '"User".user_id, user_first_name, user_last_name, user_phone, user_email, delivery_direction,' \
                'delivery_municipality, "Dispensary".dispensary_id, dispensary_name, dispensary_phone,' \
                'dispensary_email, dispensary_direction, dispensary_municipality from "User" inner join "Purchase" ' \
                'on "User".user_id = "Purchase".user_id inner join "Delivery" on ' \
                '"Purchase".purchase_id = "Delivery".purchase_id inner join "Dispensary" on ' \
                '"Purchase".dispensary_id = "Dispensary".dispensary_id where delivery_id = %s order by purchase_date;'
        cursor.execute(query, (delivery_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def getDeliveryByUser(self, user_id):
        cursor = self.conn.cursor()
        query = 'select * from "Delivery" natural inner join "User" where user_id = %s'
        cursor.execute(query, (user_id,))
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

    def updateDeliveryDriver(self, delivery_id, driver_id):
        cursor = self.conn.cursor()
        query = 'update "Delivery" set driver_id = %s where delivery_id = %s'
        cursor.execute(query, (driver_id, delivery_id))
        self.conn.commit()
        cursor.close()
        return cursor.rowcount != 0
