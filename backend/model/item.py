import os

import psycopg2


class ItemDAO:
    def __init__(self):
        self.conn = psycopg2.connect(os.getenv('DATABASE_URL'))

    # ----------------------------------------------------------------------------------------------------------------
    #                                                     Create                                                     #
    # ----------------------------------------------------------------------------------------------------------------
    def createItem(self, item_name, item_description, item_quantity, item_price, item_category, item_type,
                   dispensary_id, item_picture):
        cursor = self.conn.cursor()
        query = 'insert into "Item" (item_name, item_description, item_quantity, item_price, item_category,' \
                'item_type, dispensary_id, item_picture) values (%s, %s, %s, %s, %s, %s, %s, %s) returning item_id'
        cursor.execute(query, (item_name, item_description, item_quantity, item_price, item_category, item_type,
                               dispensary_id, item_picture))
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

    def getTotalOfItemsInStockAtDispensary(self, dispensary_id):
        cursor = self.conn.cursor()
        query = 'select count(item_id) from "Item" where dispensary_id = %s and item_quantity > 0 and item_active = True;'
        cursor.execute(query, (dispensary_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def getTotalOfItemsOutOfStockAtDispensary(self, dispensary_id):
        cursor = self.conn.cursor()
        query = 'select count(item_id) from "Item" where dispensary_id = %s and item_quantity = 0 and item_active = True;'
        cursor.execute(query, (dispensary_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def getAllActiveItems(self):
        cursor = self.conn.cursor()
        query = 'select * from "Item" where item_quantity > 0 and item_active = True;'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def getItemAtDispensary(self, dispensary_id, item_id):
        cursor = self.conn.cursor()
        query = 'select * from "Item" where dispensary_id = %s and item_id = %s and item_active = True;'
        cursor.execute(query, (dispensary_id, item_id,))
        result = cursor.fetchone()
        return result

    def getAllItemsAtDispensary(self, dispensary_id):
        cursor = self.conn.cursor()
        query = 'select * from "Item" where dispensary_id = %s and item_active = True;'
        cursor.execute(query, (dispensary_id,))
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def getItemByCategory(self, item_category):
        cursor = self.conn.cursor()
        query = 'select * from "Item" where item_category = %s and item_active = True;'
        cursor.execute(query, (item_category,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def getItemById(self, item_id):
        cursor = self.conn.cursor()
        query = 'select * from "Item" where item_id = %s and item_active = True;'
        cursor.execute(query, (item_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def getDeletedItemById(self, item_id):
        cursor = self.conn.cursor()
        query = 'select * from "Item" where item_id = %s and item_active = False;'
        cursor.execute(query, (item_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def getItemByPriceRange(self, item_price_bottom, item_price_top):
        cursor = self.conn.cursor()
        query = 'select * from "Item" where (item_price between %s and %s) and item_active = true;'
        cursor.execute(query, (item_price_bottom, item_price_top))
        result = cursor.fetchone()
        cursor.close()
        return result

    def getItemByFilter(self, item_filter_name, item_filter_description, item_filter_category, item_filter_type):
        cursor = self.conn.cursor()
        query = 'select * from "Item" where (item_name like %s or item_description like %s or item_category like %s ' \
                'or item_type like %s) and item_active = true;'
        cursor.execute(query, ('%' + item_filter_name + '%', '%' + item_filter_description + '%', '%' +
                               item_filter_category + '%', '%' + item_filter_type + '%',))
        result = cursor.fetchone()
        cursor.close()
        return result

    def getItemQuantityById(self, item_id):
        cursor = self.conn.cursor()
        query = 'select (item_quantity) from "Item" where item_id = %s;'
        cursor.execute(query, (item_id,))
        result = cursor.fetchone()[0]
        cursor.close()
        return result

    def getItemPriceById(self, item_id):
        cursor = self.conn.cursor()
        query = 'select (item_price) from "Item" where item_id = %s;'
        cursor.execute(query, (item_id,))
        result = cursor.fetchone()[0]
        cursor.close()
        return result

    # ----------------------------------------------------------------------------------------------------------------
    #                                                    Update                                                      #
    # ----------------------------------------------------------------------------------------------------------------
    def updateItemData(self, dispensary_id, item_id, item_name, item_description, item_price, item_category, item_type):
        cursor = self.conn.cursor()
        query = 'update "Item" set item_name = %s, item_description = %s, item_price = %s, ' \
                'item_category = %s, item_type = %s where dispensary_id = %s and item_id = %s'
        cursor.execute(query, (item_name, item_description, item_price, item_category, item_type, dispensary_id,
                               item_id,))
        self.conn.commit()
        cursor.close()
        return cursor.rowcount != 0

    def updateItemPicture(self, item_id, item_picture):
        cursor = self.conn.cursor()
        query = 'update "Item" set item_picture = %s where item_id = %s'
        cursor.execute(query, (item_picture, item_id,))
        self.conn.commit()
        cursor.close()
        return cursor.rowcount != 0

    def updateItemQuantity(self, item_id, item_quantity):
        cursor = self.conn.cursor()
        query = 'update "Item" set item_quantity = %s where item_id = %s'
        cursor.execute(query, (item_quantity, item_id,))
        self.conn.commit()
        cursor.close()
        return cursor.rowcount != 0

    # ----------------------------------------------------------------------------------------------------------------
    #                                                    Delete                                                      #
    # ----------------------------------------------------------------------------------------------------------------
    def deleteItemAtDispensary(self, dispensary_id, item_id):
        cursor = self.conn.cursor()
        query = 'update "Item" set item_active = False where dispensary_id = %s and item_id = %s'
        cursor.execute(query, (dispensary_id, item_id,))
        self.conn.commit()
        cursor.close()
        return cursor.rowcount != 0
