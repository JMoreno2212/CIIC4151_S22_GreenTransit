import os

import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash


class UserDAO:
    def __init__(self):
        self.conn = psycopg2.connect(os.getenv('DATABASE_URL'))

    # ----------------------------------------------------------------------------------------------------------------
    #                                                     Create                                                     #
    # ----------------------------------------------------------------------------------------------------------------
    def createUser(self, user_first_name, user_last_name, user_birth_date, user_phone, user_email, user_password,
                   license_id, user_picture):
        cursor = self.conn.cursor()
        query = 'insert into "User" (user_first_name, user_last_name, user_birth_date, user_phone, user_email, ' \
                'user_password, license_id, user_picture) values (%s, %s, %s, %s, %s, %s, %s, %s) returning user_id'
        cursor.execute(query, (user_first_name, user_last_name, user_birth_date, user_phone, user_email,
                               generate_password_hash(user_password), license_id, user_picture))
        user_id = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        return user_id

    # ----------------------------------------------------------------------------------------------------------------
    #                                                     Delete                                                     #
    # ----------------------------------------------------------------------------------------------------------------
    def deleteUser(self, user_id):
        cursor = self.conn.cursor()
        query = 'update "User" set user_active = False where user_id = %s'
        cursor.execute(query, (user_id,))
        self.conn.commit()
        cursor.close()
        return cursor.rowcount != 0

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

    def getAllActiveUsers(self):
        cursor = self.conn.cursor()
        query = 'select * from "User" where user_active = True;'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def getUserByEmail(self, user_email):
        cursor = self.conn.cursor()
        query = 'select * from "User" where user_email = %s and user_active = True'
        cursor.execute(query, (user_email,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def getUserById(self, user_id):
        cursor = self.conn.cursor()
        query = 'select * from "User" where user_id = %s'
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    # ----------------------------------------------------------------------------------------------------------------
    #                                                     Update                                                     #
    # ----------------------------------------------------------------------------------------------------------------
    def updateUserData(self, user_id, user_phone, user_email, user_password):
        cursor = self.conn.cursor()
        query = 'update "User" set user_phone = %s, user_email = %s, user_password = %s where user_id = %s'
        cursor.execute(query, (user_phone, user_email, generate_password_hash(user_password), user_id,))
        self.conn.commit()
        cursor.close()
        return cursor.rowcount != 0

    def updateUserPicture(self, user_id, user_picture):
        cursor = self.conn.cursor()
        query = 'update "User" set user_picture = %s where user_id = %s'
        cursor.execute(query, (user_picture, user_id,))
        self.conn.commit()
        cursor.close()
        return cursor.rowcount != 0

    def resetPassword(self, user_email, user_password):
        cursor = self.conn.cursor()
        query = 'update "User" set user_password = %s where user_email = %s'
        cursor.execute(query, (generate_password_hash(user_password), user_email))
        self.conn.commit()
        cursor.close()
        return cursor.rowcount != 0

    # ----------------------------------------------------------------------------------------------------------------
    #                                                     Login                                                      #
    # ----------------------------------------------------------------------------------------------------------------
    def verifyUserLogin(self, user_email, user_password):
        result = self.getUserByEmail(user_email)
        if not result:
            return None  # Email address does not exist
        hashed_password = result[6]
        if check_password_hash(hashed_password, user_password):
            return result
        else:
            return None  # Password is incorrect
