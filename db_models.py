from db import db
import itertools
import util

class Airline:
    def __init__(self, IATA="", ICAO=""):
        self.iata = IATA.upper()
        self.name = None
        self.icao = ICAO.upper()
        self.status = False

        self.fetch()

    def fetch(self):
        if self.iata != "" and self.icao != "":
            query = "select Name from airline where IATA = '{0}' AND ICAO = '{1}'".format(
                self.iata, self.icao)
            row = db().fetch(query)
            if row:
                self.name = row[0]
                self.status = True
        elif self.iata != "" and self.icao == "":
            query = "select Name, ICAO from airline where IATA = '{0}'".format(
                self.iata)
            row = db().fetch(query)
            if row:
                self.name = row[0]
                self.icao = row[1]
                self.status = True
        elif self.iata == "" and self.icao != "":
            query = "select Name, IATA from airline where ICAO = '{0}'".format(
                self.icao)
            row = db().fetch(query)
            if row:
                self.name = row[0]
                self.iata = row[1]
                self.status = True
    
    @staticmethod
    def commercial_airlines():
        query = "SELECT IATA FROM COMMERCIAL;"
        rows = db().fetchall(query)
        return [row[0] for row in rows]


class Airport:
    def __init__(self, IATA=""):
        self.iata = IATA
        self.name = None
        self.city = None
        self.country = None
        self.icao = None
        self.lat = None
        self.lng = None
        self.alt = None
        self.tz = None
        self.tzByNum = None
        self.status = False
        self.fetchByCode(IATA)

    def fetchByCode(self, IATA):
        query = "SELECT Name, City, Country, ICAO, Latitude, Longitude, Altitude, TimezoneType, Timezone FROM airport WHERE IATA = %s"
        #row = db().fetch(query)
        A = (IATA,)
        connection = db().connection
        cur = connection.cursor(buffered=True)
        cur.execute(query, A)
        row = cur.fetchone()
        if row:
            self.name = row[0]
            self.city = row[1]
            self.country = row[2]
            self.icao = row[3]
            self.lat = row[4]
            self.lng = row[5]
            self.alt = row[6]
            self.tz = row[7]
            self.tzByNum = row[8]
            self.status = True

    @staticmethod
    def read():
        query = "select Name, City, Country, IATA, ICAO, Latitude, Longitude, Altitude, TimezoneType, Timezone from airport"
        rows = db().fetchall(query)
        data = {"airports": []}
        for row in rows:
            airport = {}
            airport["name"] = row[0]
            airport["city"] = row[1]
            airport["country"] = row[2]
            airport["IATA"] = row[3]
            airport["ICAO"] = row[4]
            airport["lat"] = row[5]
            airport["lng"] = row[6]
            airport["alt"] = row[7]
            airport["timezone"] = row[8]
            airport["offset"] = row[9]
            data["airports"].append(airport)
        return data


class Country:
    def __init__(self, code="", name=""):
        self.code = code
        self.name = name

        if code and not name:
            self.fetch(code)
        elif name and not code:
            self.fetchByName()
        elif name and code:
            self.fetch(code)

    def fetchByName(self):
        if self.name:
            query = "select ISO2 from country where Name = '{0}'".format(
                self.name)
            row = db().fetch(query)
            self.code = row[0]

    def fetch(self, code):
        if code:
            query = "select Name from country where ISO2 = '{0}'".format(code)
            row = db().fetch(query)
            if row:
                self.name = row[0]

class Aircraft:
    def __init__(self, IATA="", ICAO=""):
        self.IATA = IATA
        self.ICAO = ICAO
        self.Model = ""
        self.Type = ""
        self.Size = ""
        self.Seats = ""
        self.status = False

    def fetch(self, value=""):
        if len(value) == 3:
            query = """SELECT ICAO, Model, Type, Size, Seats FROM aircraft WHERE IATA = '{0}'""".format(value)
        elif len(value) == 4:
            query = """SELECT IATA, Model, Type, Size, Seats FROM aircraft WHERE ICAO = '{0}'""".format(value)
        else:
            return None
        row = db().fetch(query)
        if row:
            if self.IATA != "":
                self.ICAO = row[0]
            elif self.ICAO != "":
                self.IATA = row[0]
            self.Model = row[1]
            self.Type = row[2]
            self.Size = row[3]
            self.Seats = row[4]
            self.status = True

class Cars:
    def __init__(self, model, zipcode):
        self.model = model
        self.zipcode = zipcode

    def fetchall(self):
        d = db()
        query = d.CARS_FULL_INFO_QUERY.format(self.model, self.zipcode, self.model, self.zipcode)
        #query = d.CARS_FULL_INFO_VIEW_QUERY.format(self.model, self.zipcode)
        data = d.fetchall(query, show_columns=True)
        columns, rows = data["columns"], data["data"]
        result = [{columns[i]: detail for i, detail in enumerate(car)} for car in rows]
        return result

    @staticmethod
    def import_view():
        d = db()
        brand_list = util.get_brand_list()
        brands = [brand_list[i] for i in ["Toyota", "Honda", "BMW", "Ford", "Acura", "Hyundai"]]
        zipcodes = ["46204", "19406", "60611"]
        brands_zipcodes = list(itertools.product(brands, zipcodes))[1:]
        for brand, zipcode in brands_zipcodes:
            query = d.CREATE_ALL_CARS_INFO_VIEW_QUERY.format(brand, zipcode, brand, zipcode, brand, zipcode)
            d.execute(query)
            print("{} {} success".format(brand,zipcode))

if __name__ == "__main__":
    Cars.import_view()
