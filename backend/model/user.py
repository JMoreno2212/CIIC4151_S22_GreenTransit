import os

import psycopg2


class UserDAO:
    def __init__(self):
        self.conn = psycopg2.connect(os.getenv('DATABASE_URL'))

    # ----------------------------------------------------------------------------------------------------------------
    #                                                      Read                                                      #
    # ----------------------------------------------------------------------------------------------------------------
    def getAllUsers(self):
        cursor = self.conn.cursor()
        query = 'select * from "User";'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def getUserById(self, user_id):
        cursor = self.conn.cursor()
        query = 'select * from "User" where user_id = %s'
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result
