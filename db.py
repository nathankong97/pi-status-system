from config import *
import mysql.connector as mysql

class db:
    def __init__(self, database="flight_data"):
        self.connection = mysql.connect(
            host="192.168.1.2",
            user=USERNAME,
            password=PASSWORD,
            database=database
        )

    def fetch(self, query):
        cur = self.connection.cursor(buffered=True)
        cur.execute(query)
        rows = cur.fetchall()