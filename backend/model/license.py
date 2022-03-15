import os

import psycopg2
from cryptography.fernet import Fernet

class LicenseDAO:
    def __init__(self):
        self.conn = psycopg2.connect(os.getenv('DATABASE_URL'))

    # ----------------------------------------------------------------------------------------------------------------
    #                                                     Create                                                     #
    # ----------------------------------------------------------------------------------------------------------------
    def createLicense(self, license_type, license_name, license_expiration, license_file):
        fernet = Fernet(os.getenv('LICENSE_KEY'))
        cursor = self.conn.cursor()
        query = 'insert into "License" (license_type, license_name, license_expiration, license_file) ' \
                'values (%s, %s, %s, %s) returning license_id'
        cursor.execute(query, (license_type, fernet.encrypt(license_name.encode()), license_expiration, license_file))
        license_id = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        return license_id

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

    def getAllActiveLicenses(self):
        cursor = self.conn.cursor()
        query = 'select * from "License" where license_active = True;'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def getLicenseByName(self, license_name):
        fernet = Fernet(os.getenv('LICENSE_KEY'))
        cursor = self.conn.cursor()
        query = 'select * from "License" where license_name = %s'
        cursor.execute(query, (fernet.encrypt(license_name.encode()),))
        result = cursor.fetchone()
        cursor.close()
        return result

    def getLicenseById(self, license_id):
        cursor = self.conn.cursor()
        query = 'select * from "License" where license_id = %s'
        cursor.execute(query, (license_id,))
        result = cursor.fetchone()
        cursor.close()
        return result
