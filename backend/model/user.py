import psycopg2

from backend.config.dbconfig import db_root_config


class UserDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (db_root_config['dbname'],
                                                                            db_root_config['user'],
                                                                            db_root_config['password'],
                                                                            db_root_config['dbport'],
                                                                            db_root_config['host'])
        self.conn = psycopg2.connect(connection_url)

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
