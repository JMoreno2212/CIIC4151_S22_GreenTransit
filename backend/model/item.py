import os

import psycopg2


class ItemDAO:
    def __init__(self):
        self.conn = psycopg2.connect(os.getenv('DATABASE_URL'))

    # ----------------------------------------------------------------------------------------------------------------
    #                                                     Create                                                     #
    # ----------------------------------------------------------------------------------------------------------------
    def createItem(self, item_name, item_description, item_quantity, item_price, item_category, item_type,
                   dispensary_id):
        cursor = self.conn.cursor()
        query = 'insert into "Item" (item_name, item_description, item_quantity, item_price, item_category,' \
                'item_type, dispensary_id) values (%s, %s, %s, %s, %s, %s, %s) returning item_id'
        cursor.execute(query, (item_name, item_description, item_quantity, item_price, item_category, item_type,
                               dispensary_id))
        item_id = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        return item_id

    # ----------------------------------------------------------------------------------------------------------------
    #                                                      Read                                                      #
    # ----------------------------------------------------------------------------------------------------------------
    def getAllItems(self):
        cursor = self.conn.cursor()
        query = 'select * from "Item";'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def getAllActiveItems(self):
        cursor = self.conn.cursor()
        query = 'select * from "Item" where item_active = True;'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def getItemById(self, item_id):
        cursor = self.conn.cursor()
        query = 'select * from "Item" where item_id = %s;'
        cursor.execute(query, (item_id,))
        result = cursor.fetchone()
        return result

    def getItemsByDispensary(self, dispensary_id):
        cursor = self.conn.cursor()
        query = 'select * from "Item" where dispensary_id = %s;'
        cursor.execute(query, (dispensary_id,))
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result
