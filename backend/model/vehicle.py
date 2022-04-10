import os

import psycopg2


class VehicleDAO:
    def __init__(self):
        self.conn = psycopg2.connect(os.getenv('DATABASE_URL'))

    # ----------------------------------------------------------------------------------------------------------------
    #                                                     Create                                                     #
    # ----------------------------------------------------------------------------------------------------------------
    def createVehicle(self, vehicle_plate, vehicle_brand, vehicle_model, vehicle_year, driver_id, license_id):
        cursor = self.conn.cursor()
        query = 'insert into "Vehicle" (vehicle_plate, vehicle_brand, vehicle_model, vehicle_year, driver_id,' \
                'license_id) values (%s, %s, %s, %s, %s, %s) returning vehicle_id'
        cursor.execute(query, (vehicle_plate, vehicle_brand, vehicle_model, vehicle_year, driver_id, license_id,))
        vehicle_id = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        return vehicle_id

    # ----------------------------------------------------------------------------------------------------------------
    #                                                     Delete                                                     #
    # ----------------------------------------------------------------------------------------------------------------
    def deleteVehicle(self, vehicle_id):
        cursor = self.conn.cursor()
        query = 'update "Vehicle" set vehicle_active = False where vehicle_id = %s'
        cursor.execute(query, (vehicle_id,))
        self.conn.commit()
        cursor.close()
        return True

    # ----------------------------------------------------------------------------------------------------------------
    #                                                      Read                                                      #
    # ----------------------------------------------------------------------------------------------------------------
    def getAllVehicles(self):
        cursor = self.conn.cursor()
        query = 'select * from "Vehicle";'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def getAllActiveVehicles(self):
        cursor = self.conn.cursor()
        query = 'select * from "Vehicle" where vehicle_active = True;'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def getVehicleByDriver(self, driver_id):
        cursor = self.conn.cursor()
        query = 'select * from "Vehicle" where driver_id = %s;'
        cursor.execute(query, (driver_id,))
        result = cursor.fetchone()
        return result

    def getVehicleById(self, vehicle_id):
        cursor = self.conn.cursor()
        query = 'select * from "Vehicle" where vehicle_id = %s;'
        cursor.execute(query, (vehicle_id,))
        result = cursor.fetchone()
        return result
