import os

import psycopg2


class ItemDAO:
    def __init__(self):
        self.conn = psycopg2.connect(os.getenv('DATABASE_URL'))

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

    def getItemById(self, item_id):
        cursor = self.conn.cursor()
        query = 'select * from "Item" where item_id = %s;'
        cursor.execute(query, (item_id,))
        result = cursor.fetchone()
        return result
