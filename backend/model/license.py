import os

import psycopg2


class LicenseDAO:
    def __init__(self):
        self.conn = psycopg2.connect(os.getenv('DATABASE_URL'))

    # ----------------------------------------------------------------------------------------------------------------
    #                                                      Read                                                      #
    # ----------------------------------------------------------------------------------------------------------------
    def getAllLicenses(self):
        cursor = self.conn.cursor()
        query = 'select * from "License";'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def getLicenseById(self, license_id):
        cursor = self.conn.cursor()
        query = 'select * from "License" where license_id = %s'
        cursor.execute(query, (license_id,))
        result = cursor.fetchone()
        cursor.close()
        return result
