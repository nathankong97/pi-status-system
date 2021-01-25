from config import *
import mysql.connector as mysql
from queries import queries

class db(queries):
    def __init__(self, database="flight_data"):
        self.connection = mysql.connect(
            host=IP,
            user=USERNAME,
            password=PASSWORD,
            database=database
        )

    def execute(self, query):
        cur = self.connection.cursor(buffered=True)
        cur.execute(query)

    def fetch(self, query):
        cur = self.connection.cursor(buffered=True)
        cur.execute(query)
        row = cur.fetchone()
        return row[0]

    def fetchall(self, query, show_columns=False):
        cur = self.connection.cursor(buffered=True)
        cur.execute(query)
        rows = cur.fetchall()
        if show_columns:
            return {
                "columns": [i[0] for i in cur.description],
                "data": rows
            }
        else:
            return rows

    def db_usage(self):
        cur = self.connection.cursor(buffered=True)
        cur.execute(self.DB_USAGE_QUERY)
        rows = cur.fetchall()
        return rows
    
    def table_usage(self, db_name):
        cur = self.connection.cursor(buffered=True)
        cur.execute(self.TABLE_USAGE_QUERY.format(db_name))
        rows = cur.fetchall()
        return rows

    def show_columns(self, query):
        cur = self.connection.cursor(buffered=True)
        if query[-1] == ";":
            query = query[:-1]
        new_query = query + " LIMIT 1;"
        cur.execute(query)
        return [i[0] for i in cur.description]

if __name__ == "__main__":
    d = db()
    query = d.COORDINATE_BY_AIRPORT_QUERY.format("IND")
    data = d.fetch(query)
    print(data)