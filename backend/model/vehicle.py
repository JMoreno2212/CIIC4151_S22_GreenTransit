import os

import psycopg2


class VehicleDAO:
    def __init__(self):
        self.conn = psycopg2.connect(os.getenv('DATABASE_URL'))

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

    def getVehicleById(self, vehicle_id):
        cursor = self.conn.cursor()
        query = 'select * from "Vehicle" where vehicle_id = %s;'
        cursor.execute(query, (vehicle_id,))
        result = cursor.fetchone()
        return result
