import os

import psycopg2


class DispensaryDAO:
    def __init__(self):
        self.conn = psycopg2.connect(os.getenv('DATABASE_URL'))

    # ----------------------------------------------------------------------------------------------------------------
    #                                                      Read                                                      #
    # ----------------------------------------------------------------------------------------------------------------
    def getAllDispensaries(self):
        cursor = self.conn.cursor()
        query = 'select * from "Dispensary";'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def getDispensaryById(self, dispensary_id):
        cursor = self.conn.cursor()
        query = 'select * from "Dispensary" where dispensary_id = %s;'
        cursor.execute(query, (dispensary_id,))
        result = cursor.fetchone()
        return result
