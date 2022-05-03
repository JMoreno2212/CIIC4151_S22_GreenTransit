import os

import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash


class DriverDAO:
    def __init__(self):
        self.conn = psycopg2.connect(os.getenv('DATABASE_URL'))

    # ----------------------------------------------------------------------------------------------------------------
    #                                                     Create                                                     #
    # ----------------------------------------------------------------------------------------------------------------
    def createDriver(self, driver_first_name, driver_last_name, driver_birth_date, driver_phone, driver_email,
                     driver_password, driver_driving_license, driver_gmp_certificate, driver_dispensary_technician,
                     occupational_license_id, driver_picture):
        cursor = self.conn.cursor()
        query = 'insert into "Driver" (driver_first_name, driver_last_name, driver_birth_date, driver_phone,' \
                'driver_email, driver_password, driver_driving_license, driver_gmp_certificate,' \
                'driver_dispensary_technician, occupational_license_id, driver_picture) ' \
                'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning driver_id'
        cursor.execute(query, (driver_first_name, driver_last_name, driver_birth_date, driver_phone, driver_email,
                               generate_password_hash(driver_password), driver_driving_license, driver_gmp_certificate,
                               driver_dispensary_technician, occupational_license_id, driver_picture))
        driver_id = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        return driver_id

    # ----------------------------------------------------------------------------------------------------------------
    #                                                     Delete                                                     #
    # ----------------------------------------------------------------------------------------------------------------
    def deleteDriver(self, driver_id):
        cursor = self.conn.cursor()
        query = 'update "Driver" set driver_active = False where driver_id = %s'
        cursor.execute(query, (driver_id,))
        self.conn.commit()
        cursor.close()
        return cursor.rowcount != 0

    # ----------------------------------------------------------------------------------------------------------------
    #                                                      Read                                                      #
    # ----------------------------------------------------------------------------------------------------------------
    def getAllDrivers(self):
        cursor = self.conn.cursor()
        query = 'select * from "Driver";'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def getAllActiveDrivers(self):
        cursor = self.conn.cursor()
        query = 'select * from "Driver" where driver_active = True;'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def getDriverByEmail(self, driver_email):
        cursor = self.conn.cursor()
        query = 'select * from "Driver" where driver_email = %s and driver_active = True'
        cursor.execute(query, (driver_email,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def getDriverById(self, driver_id):
        cursor = self.conn.cursor()
        query = 'select * from "Driver" where driver_id = %s;'
        cursor.execute(query, (driver_id,))
        result = cursor.fetchone()
        return result

    def getAllDriverDeliveries(self, driver_id):
        cursor = self.conn.cursor()
        query = 'select delivery_id, "Driver".driver_id, "Purchase".purchase_id, purchase_number, purchase_date,' \
                '"User".user_id, user_first_name, user_last_name, user_phone, user_email, delivery_direction,' \
                'delivery_municipality, "Dispensary".dispensary_id, dispensary_name, dispensary_phone,' \
                'dispensary_email, dispensary_direction, dispensary_municipality, driver_first_name,' \
                'driver_last_name, delivery_status from "User" inner join "Purchase" ' \
                'on "User".user_id = "Purchase".user_id inner join "Delivery" on ' \
                '"Purchase".purchase_id = "Delivery".purchase_id inner join "Dispensary" on ' \
                '"Purchase".dispensary_id = "Dispensary".dispensary_id inner join "Driver" on ' \
                '"Driver".driver_id = "Delivery".driver_id where "Driver".driver_id = %s order by purchase_date;'
        cursor.execute(query, (driver_id,))
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def getAllPastDriverDeliveries(self, driver_id):
        cursor = self.conn.cursor()
        query = 'select delivery_id, "Driver".driver_id, "Purchase".purchase_id, purchase_number, purchase_date,' \
                '"User".user_id, user_first_name, user_last_name, user_phone, user_email, delivery_direction,' \
                'delivery_municipality, "Dispensary".dispensary_id, dispensary_name, dispensary_phone,' \
                'dispensary_email, dispensary_direction, dispensary_municipality, driver_first_name,' \
                'driver_last_name, delivery_status from "User" inner join "Purchase" ' \
                'on "User".user_id = "Purchase".user_id inner join "Delivery" on ' \
                '"Purchase".purchase_id = "Delivery".purchase_id inner join "Dispensary" on ' \
                '"Purchase".dispensary_id = "Dispensary".dispensary_id inner join "Driver" on ' \
                '"Driver".driver_id = "Delivery".driver_id where "Driver".driver_id = %s and delivery_status = ' \
                '\'Delivered\' order by purchase_date;'
        cursor.execute(query, (driver_id,))
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    # ----------------------------------------------------------------------------------------------------------------
    #                                                     Update                                                     #
    # ----------------------------------------------------------------------------------------------------------------
    def updateDriverData(self, driver_id, driver_phone, driver_email, driver_password):
        cursor = self.conn.cursor()
        query = 'update "Driver" set driver_phone = %s, driver_email = %s, driver_password = %s where driver_id = %s'
        cursor.execute(query, (driver_phone, driver_email, generate_password_hash(driver_password), driver_id,))
        self.conn.commit()
        cursor.close()
        return cursor.rowcount != 0

    def updateDriverPicture(self, driver_id, driver_picture):
        cursor = self.conn.cursor()
        query = 'update "Driver" set driver_picture = %s where driver_id = %s'
        cursor.execute(query, (driver_picture, driver_id,))
        self.conn.commit()
        cursor.close()
        return cursor.rowcount != 0

    def resetPassword(self, driver_email, driver_password):
        cursor = self.conn.cursor()
        query = 'update "Driver" set driver_password = %s where driver_email = %s'
        cursor.execute(query, (generate_password_hash(driver_password), driver_email))
        self.conn.commit()
        cursor.close()
        return cursor.rowcount != 0

    # ----------------------------------------------------------------------------------------------------------------
    #                                                     Login                                                      #
    # ----------------------------------------------------------------------------------------------------------------
    def verifyDriverLogin(self, driver_email, driver_password):
        result = self.getDriverByEmail(driver_email)
        if not result:
            return None  # Email address does not exist
        hashed_password = result[6]
        if check_password_hash(hashed_password, driver_password):
            return result
        else:
            return None  # Password is incorrect
