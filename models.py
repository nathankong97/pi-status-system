from fake_useragent import UserAgent
import requests, time, random, datetime, os, pytz
import util
from multiprocessing.pool import Pool
from as_config import AirportSchedule_Config
from as_helpers import AirportSchedule_Helpers
from db_models import Airport, Airline, Country

class AirportSchedule(AirportSchedule_Config, AirportSchedule_Helpers):
    def __init__(self, code, mode, proxy=None):
        self.code = code
        self.proxy = proxy
        self.header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
        }
        self.url = "https://api.flightradar24.com/common/v1/airport.json"
        self.start_time, self.end_time = self.getStartEndTime()
        self.params = { 
            "code": self.code,
            "plugin-setting[schedule][timestamp]": self.start_time if self.start_time else None,
            "page": 1,
            "limit": 100,
            "plugin[]": "schedule",
            "plugin-setting[schedule][mode]": "departures"
        }

    @util.timing
    def getStartEndTime(self):
        proxy = {"http": random.choice(self.proxy)} if self.proxy else None
        time_params = {
            "code": self.code,
            "plugin[]": "details"
        }
        try:
            r = requests.get(self.url, params=time_params,
                             timeout=15, proxies=proxy, headers=self.header)
        except:
            return None
        if r.status_code == 200:
            offset = r.json()[
                "result"]["response"]["airport"]["pluginData"]["details"]["timezone"]["offset"]
            current_time_with_time_zone = int(
                time.mktime(time.gmtime())) + offset
            date = datetime.datetime.fromtimestamp(current_time_with_time_zone)
            start_of_day = datetime.datetime(
                date.year, date.month, date.day, 0, 0, 0, tzinfo=pytz.UTC)
            end_of_day = datetime.datetime(
                date.year, date.month, date.day + 1, 0, 0, 0, tzinfo=pytz.UTC)
            return util.convertDateTimeToUnix(start_of_day) - offset, util.convertDateTimeToUnix(end_of_day) - offset
        else:
            print(r.status_code)

    def __getListOfParams(self):
        return [dict(self.params, page=i) for i in range(1, 16)]

    def getDetails(self):
        proxy = {"http": random.choice(self.proxy)} if self.proxy else None
        url = "https://api.flightradar24.com/common/v1/airport.json?code={}&plugin[]=details&plugin[]=runways".format(self.code)
        r = requests.get(url, timeout=15, proxies=proxy, headers=self.header)
        if r.status_code == 200:
            return r.json()
        else:
            return None

    @util.timing
    def getData(self):
        list_params = self.__getListOfParams()
        pool = Pool(os.cpu_count())
        data = [flight for flights in pool.map(self.parseJson, list_params) for flight in flights
                if self.checkBeforeEndTime(flight) and self.checkCargo(flight)]
        offset = data[0]["flight"]["airport"]["origin"]["timezone"]["offset"]
        Flight_data = pool.map(Flight, data)
        return {"flights": data}
        #return {"origin": self.code.upper(), "flights": [i.dictionary() for i in Flight_data], "offset": offset}

    @util.timing
    def getData2(self):
        list_params = self.__getListOfParams()
        pool = Pool(os.cpu_count())
        flightList = [flight for flights in pool.map(self.parseJson, list_params) for flight in flights
                if self.checkBeforeEndTime(flight) and self.checkCargo(flight)]
        offset = flightList[0]["flight"]["airport"]["origin"]["timezone"]["offset"]
        tz = Airport(self.code).tzByNum
        dst = flightList[0]["flight"]["airport"]["origin"]["timezone"]["isDst"]
        flightList = [{
            "flightNum": i["flight"]["identification"]["number"]["default"],
            "time": util.convertUnixToTimeStamp(i["flight"]["time"]["scheduled"]["departure"], tz, dst),
            "flightTime": util.convertSecondToHour(
                i["flight"]["time"]["scheduled"]["arrival"] - i["flight"]["time"]["scheduled"]["departure"]),
            "actualTime": util.convertUnixToTimeStamp(
                i["flight"]["time"]["real"]["departure"], tz, dst),
            "airline": self.setValueforAirline(i),
            "aircraft": self.setValueforAircraft(i),
            "airlineIATA": self.setValueforAirlineIATA(i),
            "destinationCity": self.setValueforCity(i),
            "destinationAirport": self.setValueforDestinationAirport(i),
            "destinationCountry": self.setValueforCountry(i),
            "destinationCountryCode": self.setValueforCountryCode(i),
            "destinationIATA": self.setValueforDestinationIATA(i),
            "gate": i["flight"]["airport"]["origin"]["info"]["gate"],
            "status": i["flight"]["status"]["text"]
        } for i in flightList
            if i is not None]
        flightList = [dict(t) for t in {tuple(d.items()) for d in flightList}]
        return {"origin": self.code.upper(), "flights": flightList, "offset": offset, "dst": dst}
    
    @util.timing
    def getCurrentData(self):
        local_param = self.params
        local_param["plugin-setting[schedule][timestamp]"] = None
        local_param["limits"] = 40
        data = [Flight(i).dictionary() for i in self.parseJson(local_param) if self.checkCargo(i)]
        tz = Airport(self.code).tzByNum
        dst = data[0]["origin_offset_dst"]
        #data_withtime = [flight.__setitem__("sched_dep", util.convertUnixToTimeStamp(flight["sched_dep"], tz, dst)) for flight in data]
        [data[i].update({"sched_dep": util.convertUnixToTimeStamp(data[i]["sched_dep"], tz, dst)}) for i in range(len(data))]
        return {"flights": data}
        
    @util.timing
    def getAirportWeather(self):
        local_param = self.params
        local_param["plugin-setting[schedule][timestamp]"] = None
        local_param["limits"] = 1
        local_param["plugin-setting[schedule][mode]"] = None
        local_param["plugin[]"] = None
        attempt = 1
        while attempt < 5:
            try:
                proxy = {"http": random.choice(self.proxy)} if self.proxy else None
                #return requests.get(self.url, params=local_param, timeout=15, proxies=proxy, headers=self.header).json()
                return requests.get(self.url, params=local_param, timeout=15, proxies=proxy, headers=self.header).json()["result"]["response"]["airport"]["pluginData"]["weather"]
            except:
                attempt += 1
        return
        

    def checkBeforeEndTime(self, flight):
        return flight["flight"]["time"]["scheduled"]["departure"] <= self.end_time

    def parseJson(self, params):
        status_mode = self.params["plugin-setting[schedule][mode]"]
        attempt = 1
        while attempt < 5:
            try:
                proxy = {"http": random.choice(self.proxy)} if self.proxy else None
                return requests.get(self.url, params=params, timeout=15, proxies=proxy, headers=self.header).json()["result"]["response"]["airport"]["pluginData"]["schedule"][status_mode]["data"]
            except:
                attempt += 1
        return
        

    def checkCargo(self, flight):
        def AirlineName(flight):
            try:
                return flight["flight"]["airline"]["name"]
            except:
                return "-"

        def AirlineIATA(flight):
            try:
                return flight["flight"]["airline"]["code"]["iata"]
            except:
                return "-"

        def AircraftIATA(flight):
            try:
                return flight["flight"]["aircraft"]["model"]["code"]
            except:
                return "-"
        name, iata, aircraftiata = AirlineName(
            flight), AirlineIATA(flight), AircraftIATA(flight)
        try:
            if any(i in name for i in self.cargoNameList) or any(i in iata for i in self.cargoIATAList) or any(i in aircraftiata for i in self.cargoAircraftList):
                return False
            else:
                return True
        except:
            return True


class Flight:
    def __init__(self, data):
        data = data["flight"]
        self.id = util.get(data, ["identification", "row"])
        self.flight_num = util.get(
            data, ["identification", "number", "default"])
        self.status_detail = util.get(data, ["status", "text"])
        self.aircraft_code = util.get(data, ["aircraft", "model", "code"])
        self.aircraft_text = util.get(data, ["aircraft", "model", "text"])
        self.aircraft_reg = util.get(data, ["aircraft", "registration"])
        self.aircraft_co2 = util.get(data, ["aircraft", "country", "alpha2"])
        self.aircraft_restr = util.get(data, ["aircraft", "restricted"])
        self.owner = util.get(data, ["owner", "name"])
        self.owner_iata = util.get(data, ["owner", "code", "iata"])
        self.owner_icao = util.get(data, ["owner", "code", "icao"])
        self.airline = util.get(data, ["airline", "name"])
        self.airline_iata = util.get(data, ["airline", "code", "iata"])
        self.airline_icao = util.get(data, ["airline", "code", "icao"])
        self.origin_offset = util.get(
            data, ["airport", "origin", "timezone", "offset"])
        self.origin_offset_abbr = util.get(
            data, ["airport", "origin", "timezone", "abbr"])
        self.origin_offset_dst = util.get(
            data, ["airport", "origin", "timezone", "isDst"])
        self.origin_terminal = util.get(
            data, ["airport", "origin", "info", "terminal"])
        self.origin_gate = util.get(
            data, ["airport", "origin", "info", "gate"])
        self.dest_iata = util.get(
            data, ["airport", "destination", "code", "iata"])
        self.dest_icao = util.get(
            data, ["airport", "destination", "code", "icao"])
        self.dest_name = util.get(data, ["airport", "destination", "name"])
        self.dest_city = util.get(
            data, ["airport", "destination", "position", "region", "city"])
        self.dest_country = util.get(
            data, ["airport", "destination", "position", "country", "name"])
        self.dest_country_code = util.get(
            data, ["airport", "destination", "position", "country", "code"])
        self.dest_offset = util.get(
            data, ["airport", "destination", "timezone", "offset"])
        self.dest_offset_abbr = util.get(
            data, ["airport", "destination", "timezone", "abbr"])
        self.dest_offset_dst = util.get(
            data, ["airport", "destination", "timezone", "isDst"])
        self.dest_terminal = util.get(
            data, ["airport", "destination", "info", "terminal"])
        self.dest_gate = util.get(
            data, ["airport", "destination", "info", "gate"])
        self.sched_dep = util.get(data, ["time", "scheduled", "departure"])
        self.sched_arr = util.get(data, ["time", "scheduled", "arrival"])
        self.real_dep = util.get(data, ["time", "real", "departure"])
        self.real_arr = util.get(data, ["time", "real", "arrival"])
        self.dest_lat = util.get(
            data, ["airport", "destination", "position", "latitude"])
        self.dest_lng = util.get(
            data, ["airport", "destination", "position", "longitude"])

    def key_list(self):
        return list(self.__dict__.keys())

    def value_list(self):
        return list(self.__dict__.values())

    def dictionary(self):
        return self.__dict__

if __name__ == "__main__":
    from proxy import Proxy
    proxy = Proxy().ip_proxies
    AS = AirportSchedule("PHL", 0, proxy=proxy)
    data = AS.getAirportWeather()
    print(data)
    #util.pprint(data)
    # f = Flight(data)
    print("---------")
    # util.pprint(f.dictionary())
