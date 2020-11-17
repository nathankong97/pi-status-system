from config import *
import mysql.connector as mysql

class db:
    def __init__(self, database="flight_data"):
        self.connection = mysql.connect(
            host=IP,
            user=USERNAME,
            password=PASSWORD,
            database=database
        )

    def fetch(self, query):
        cur = self.connection.cursor(buffered=True)
        cur.execute(query)
        row = cur.fetchone()
        return row

    def fetchall(self, query):
        cur = self.connection.cursor(buffered=True)
        cur.execute(query)
        rows = cur.fetchall()
        return rows

if __name__ == "__main__":
    d = db()
    rows = d.fetch("select Name, ICAO from Airline where IATA = 'NH';")
    print(rows)