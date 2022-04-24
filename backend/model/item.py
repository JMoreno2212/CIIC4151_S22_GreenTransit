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

    def getAllItemsAtDispensary(self, dispensary_id):
        cursor = self.conn.cursor()
        query = 'select * from "Item" where dispensary_id = %s;'
        cursor.execute(query, (dispensary_id,))
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    # def getItemByName(self, item_name):
    #     cursor = self.conn.cursor()
    #     args = ("%" + item_name + "%",)
    #     query = 'select * from "Item" where item_name like;',
    #     cursor.execute(query, (item_name, args,))
    #     result = cursor.fetchone()
    #     return result
    #
    # def getItemByCategory(self, item_category):
    #     cursor = self.conn.cursor()
    #     query = 'select * from "Item" where item_category = %s;'
    #     cursor.execute(query, (item_category,))
    #     result = cursor.fetchone()
    #     return result
    #
    # def getItemByType(self, item_type):
    #     cursor = self.conn.cursor()
    #     query = 'select * from "Item" where item_type = %s;'
    #     cursor.execute(query, (item_type,))
    #     result = cursor.fetchone()
    #     return result

    def getItemByPriceRange(self, item_price_bottom, item_price_top):
        cursor = self.conn.cursor()
        query = 'select * from "Item" where (item_price between %s and %s) and item_active = true; ;'
        cursor.execute(query, (item_price_bottom, item_price_top))
        result = cursor.fetchone()
        return result

    def getItemByFilter(self, item_filter_name, item_filter_description, item_filter_category, item_filter_type):
        cursor = self.conn.cursor()
        query = 'select * from "Item" where (item_name like %s or item_description like %s or item_category like %s ' \
                'or item_type like %s) and item_active = true;'
        cursor.execute(query, ('%' + item_filter_name + '%', '%' + item_filter_description + '%', '%' + item_filter_category + '%', '%' + item_filter_type + '%',))
        result = cursor.fetchone()
        return result

    # ----------------------------------------------------------------------------------------------------------------
    #                                                    Update                                                      #
    # ----------------------------------------------------------------------------------------------------------------
    def updateItem(self, item_id, item_name, item_description, item_quantity, item_price, item_category, item_type):
        cursor = self.conn.cursor()
        query = 'update "Item" set item_name = %s, item_description = %s, item_quantity = %s, item_price = %s, ' \
                'item_category = %s, item_type = %s  where item_id = %s'
        cursor.execute(query, (item_name, item_description, item_quantity, item_price, item_category, item_type,
                               item_id,))
        self.conn.commit()
        cursor.close()
        return cursor.rowcount != 0

    # ----------------------------------------------------------------------------------------------------------------
    #                                                    Delete                                                      #
    # ----------------------------------------------------------------------------------------------------------------
    def deleteItem(self, item_id):
        cursor = self.conn.cursor()
        query = 'update "Item" set item_active = False where item_id = %s'
        cursor.execute(query, (item_id,))
        self.conn.commit()
        cursor.close()
        return cursor.rowcount != 0

    def getItemAtDispensary(self, dispensary_id, item_id):
        cursor = self.conn.cursor()
        query = 'select * from "Item" where item_id = %s and dispensary_id = %s;'
        cursor.execute(query, (item_id, dispensary_id,))
        result = cursor.fetchone()
        return result
