from fake_useragent import UserAgent
import requests, time, random
import datetime, os, pytz
import util
from multiprocessing.pool import Pool
from as_config import AirportSchedule_Config

class AirportSchedule(AirportSchedule_Config):
    def __init__(self, code, mode, proxy = None):
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
			"plugin-setting[schedule][mode]": "departures" if mode == 0 else "arrivals"
		}

    @util.timing
    def getStartEndTime(self):
        proxy = {"http": random.choice(self.proxy)} if self.proxy else None
        time_params = {
            "code": self.code,
            "plugin[]": "details"
        }
        try:
            r = requests.get(self.url, params=time_params, timeout=15, proxies=proxy, headers=self.header)
        except:
            return None
        if r.status_code == 200:
            offset = r.json()["result"]["response"]["airport"]["pluginData"]["details"]["timezone"]["offset"]
            current_time_with_time_zone = int(time.mktime(time.gmtime())) + offset
            date = datetime.datetime.fromtimestamp(current_time_with_time_zone)
            start_of_day = datetime.datetime(date.year, date.month, date.day, 0, 0, 0, tzinfo=pytz.UTC)
            end_of_day = datetime.datetime(date.year, date.month, date.day + 1, 0, 0, 0, tzinfo=pytz.UTC)
            return util.convertDateTimeToUnix(start_of_day) - offset, util.convertDateTimeToUnix(end_of_day) - offset
        else:
            print(r.status_code)

    def __getListOfParams(self):
        return [dict(self.params, page=i) for i in range(1, 16)]

    @util.timing
    def getData(self):
        list_params = self.__getListOfParams()
        pool = Pool(os.cpu_count())
        data = [Flight(flight).dictionary() for flights in pool.map(self.parseJson, list_params) for flight in flights 
        if self.checkBeforeEndTime(flight) and self.checkCargo(flight)]
        return {"flights": data}
    
    def checkBeforeEndTime(self, flight):
        return flight["flight"]["time"]["scheduled"]["departure"] <= self.end_time
    
    def parseJson(self, params):
        proxy = {"http": random.choice(self.proxy)} if self.proxy else None
        status_mode = self.params["plugin-setting[schedule][mode]"]
        try:
            return requests.get(self.url, params=params, timeout=15, proxies=proxy, headers=self.header).json()["result"]["response"]["airport"]["pluginData"]["schedule"][status_mode]["data"]
        except:
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
        name, iata, aircraftiata = AirlineName(flight), AirlineIATA(flight), AircraftIATA(flight)
        try:
            if any(i in name for i in self.cargoNameList) \
            or any(i in iata for i in self.cargoIATAList) \
            or any(i in aircraftiata for i in cargoAircraftList):
                return False
            else:
                return True
        except:
            return True

class Flight:
    def __init__(self, data):
        data = data["flight"]
        self.id = util.get(data, ["identification", "row"])
        self.flight_num = util.get(data, ["identification","number","default"])
        self.status_detail = util.get(data, ["status","text"])
        self.aircraft_code = util.get(data,["aircraft", "model","code"])
        self.aircraft_text = util.get(data,["aircraft", "model","text"])
        self.aircraft_reg = util.get(data,["aircraft","registration"])
        self.aircraft_co2 = util.get(data,["aircraft","country", "alpha2"])
        self.aircraft_restr = util.get(data, ["aircraft","restricted"])
        self.owner = util.get(data, ["owner", "name"])
        self.owner_iata = util.get(data, ["owner","code","iata"])
        self.owner_icao = util.get(data, ["owner", "code", "icao"])
        self.airline = util.get(data, ["airline", "name"])
        self.airline_iata = util.get(data, ["airline", "code", "iata"])
        self.airline_icao = util.get(data, ["airline", "code", "icao"])
        self.origin_offset = util.get(data,["airport","origin","timezone","offset"])
        self.origin_offset_abbr = util.get(data,["airport","origin","timezone","abbr"])
        self.origin_offset_dst = util.get(data,["airport","origin","timezone","isDst"])
        self.origin_terminal = util.get(data,["airport","origin","info","terminal"])
        self.origin_gate = util.get(data,["airport","origin","info","gate"])
        self.dest_iata = util.get(data,["airport","destination","code","iata"])
        self.dest_icao = util.get(data, ["airport", "destination", "code", "icao"])
        self.dest_name = util.get(data, ["airport", "destination", "name"])
        self.dest_city = util.get(data, ["airport", "destination", "position", "region", "city"])
        self.dest_country = util.get(data, ["airport", "destination", "position", "country", "name"])
        self.dest_country_code = util.get(data, ["airport", "destination", "position", "country", "code"])
        self.dest_offset = util.get(data, ["airport", "destination", "timezone", "offset"])
        self.dest_offset_abbr = util.get(data, ["airport", "destination", "timezone", "abbr"])
        self.dest_offset_dst = util.get(data, ["airport", "destination", "timezone", "isDst"])
        self.dest_terminal = util.get(data, ["airport", "destination", "info", "terminal"])
        self.dest_gate = util.get(data, ["airport", "destination", "info", "gate"])
        self.sched_dep = util.get(data,["time","scheduled","departure"])
        self.sched_arr = util.get(data,["time","scheduled","arrival"])
        self.real_dep = util.get(data, ["time", "real", "departure"])
        self.real_arr = util.get(data, ["time", "real", "arrival"])
        self.dest_lat = util.get(data, ["airport","destination","position","latitude"])
        self.dest_lng = util.get(data, ["airport", "destination", "position", "longitude"])

    def key_list(self):
        return list(self.__dict__.keys())

    def value_list(self):
        return list(self.__dict__.values())
    
    def dictionary(self):
        return self.__dict__


if __name__ == "__main__":
    AS = AirportSchedule("ORD", 0)
    data = AS.getData()
    print(len(data))
        