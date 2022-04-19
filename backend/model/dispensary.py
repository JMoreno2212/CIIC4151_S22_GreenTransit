import os

import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash


class DispensaryDAO:
    def __init__(self):
        self.conn = psycopg2.connect(os.getenv('DATABASE_URL'))

    # ----------------------------------------------------------------------------------------------------------------
    #                                                     Create                                                     #
    # ----------------------------------------------------------------------------------------------------------------
    def createDispensary(self, dispensary_name, dispensary_phone, dispensary_direction, dispensary_municipality,
                         dispensary_zipcode, dispensary_email, dispensary_password, license_id):
        cursor = self.conn.cursor()
        query = 'insert into "Dispensary" (dispensary_name, dispensary_phone, dispensary_direction,' \
                'dispensary_municipality, dispensary_zipcode, dispensary_email, dispensary_password, license_id)' \
                'values (%s, %s, %s, %s, %s, %s, %s, %s) returning dispensary_id'
        cursor.execute(query, (dispensary_name, dispensary_phone, dispensary_direction, dispensary_municipality,
                               dispensary_zipcode, dispensary_email, generate_password_hash(dispensary_password),
                               license_id), )
        dispensary_id = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        return dispensary_id

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

    def getAllActiveDispensaries(self):
        cursor = self.conn.cursor()
        query = 'select * from "Dispensary" where dispensary_active = True;'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def getDispensaryByEmail(self, dispensary_email):
        cursor = self.conn.cursor()
        query = 'select * from "Dispensary" where dispensary_email = %s and dispensary_active = True;'
        cursor.execute(query, (dispensary_email,))
        result = cursor.fetchone()
        return result

    def getDispensaryById(self, dispensary_id):
        cursor = self.conn.cursor()
        query = 'select * from "Dispensary" where dispensary_id = %s;'
        cursor.execute(query, (dispensary_id,))
        result = cursor.fetchone()
        return result

    def verifyDispensaryLogin(self, dispensary_email, dispensary_password):
        result = self.getDispensaryByEmail(dispensary_email)
        if not result:
            return None  # Email address does not exist
        hashed_password = result[7]
        if check_password_hash(hashed_password, dispensary_password):
            return result
        else:
            return None  # Password is incorrect

    # ----------------------------------------------------------------------------------------------------------------
    #                                                      Update                                                      #
    # ----------------------------------------------------------------------------------------------------------------
    def updateDispensary(self, dispensary_id, dispensary_name, dispensary_phone, dispensary_direction,
                         dispensary_municipality, dispensary_zipcode,
                         dispensary_email, dispensary_password):  # REQUIRES ALL FIELDS TO BE FILLED
        cursor = self.conn.cursor()
        query = 'update "Dispensary" set dispensary_name = %s, dispensary_phone = %s, dispensary_direction = %s,' \
                'dispensary_municipality = %s, dispensary_zipcode = %s, dispensary_email = %s,' \
                'dispensary_password = %s where dispensary_id = %s'
        cursor.execute(query, (dispensary_name, dispensary_phone, dispensary_direction, dispensary_municipality,
                               dispensary_zipcode, dispensary_email, generate_password_hash(dispensary_password),
                               dispensary_id,))
        self.conn.commit()
        cursor.close()
        return cursor.rowcount != 0

    # ----------------------------------------------------------------------------------------------------------------
    #                                                      Delete                                                      #
    # ----------------------------------------------------------------------------------------------------------------
    def deleteDispensary(self, dispensary_id):
        cursor = self.conn.cursor()
        query = 'update "Dispensary" set dispensary_active = False where dispensary_id = %s'
        cursor.execute(query, (dispensary_id,))
        self.conn.commit()
        cursor.close()
        return cursor.rowcount != 0
