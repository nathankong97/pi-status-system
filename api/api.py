from flask_restful import Resource
from util import *
from flask import Response
import json, simplejson
import random
from models import AirportSchedule
from db_models import Airport, Airline, Country, Aircraft
from proxy import Proxy


class RpiStatusApi(Resource):
    def get(self):
        data = {
            "processor": getProcessInfo(),
            "ip_address": getIpAddress(),
            "memory": getMemoryUsage(),
            "uptime": getUptime(),
            "disk_usage": getDiskUsage(),
            "cpu_temp": getCelsius()["cpu_temperature"],
            "basic_info": getBasicInfo(),
            "sensor_cpu_temp": getSensorsTemp(),
            "cpu_info": getCpuInfo(),
            "system_info": getSysInfo(),
            "mac_address": getMAC(),
            "wifi_name": getWifiName(),
            "devices_on_wifi": getDevicesOnWifi(),
            "wifi_power": getWifiPower(),
            "last_login": getLastLogin()
        }
        return Response(json.dumps(data), mimetype="application/json", status=200)


class LocationApi(Resource):
    def get(self):
        #data = getLocation()
        # return Response(json.dumps(data), mimetype="application/json", status=200)
        pass


class SpeedTestApi(Resource):
    def get(self):
        data = getSpeedTest()
        return Response(json.dumps(data), mimetype="application/json", status=200)


class FlightScheduleApi(Resource):
    def get(self, id, status_code):
        proxy = Proxy().ip_proxies
        data = AirportSchedule(id, status_code, proxy=proxy).getData2()
        flights = data["flights"]

        def calculateAirlineCounts():
            airlines = [i["airlineIATA"] for i in flights if i["airlineIATA"] and i["airlineIATA"] != "-" and i["status"] not in ["Unknown","Canceled"]]
            airlineDict = {}
            for i in airlines:
                if i not in airlineDict:
                    airlineDict[i] = 1
                else:
                    airlineDict[i] += 1
            airlineDict = {k: v for k, v in sorted(airlineDict.items(), key=lambda item: item[1],reverse=True)}
            airlineList = [Airline(IATA=i).name for i in list(airlineDict.keys())][:5]
            iata = list(airlineDict.keys())[:5]
            counts = list(airlineDict.values())[:5]
            data["calculateAirlineCounts"] = {"iata": iata,"airlines":airlineList, "counts":counts}

        def calculateNumOfCanceled():
            counts = len([i for i in flights if i["status"] in ["Unknown", "Canceled"]])
            data["canceledCounts"] = counts

        def calculateTotalFlights():
            total = len(flights)
            data["totalFlights"] = total
        
        def internationalDomestic():
            homeCountry = Airport(IATA=id).country
            countryList = [i["destinationCountryCode"] for i in flights if i["status"] not in ["Unknown", "Canceled"]]
            countryList = [Country(code=i).name for i in countryList]
            domesticCount = len([i for i in countryList if i == homeCountry])
            intlCount = len(countryList) - domesticCount
            intlList = [i for i in countryList if i != homeCountry]
            countryCount = {}
            for i in intlList:
                if i not in countryCount:
                    countryCount[i] = 1
                else:
                    countryCount[i] += 1
            countryCount = {k: v for k, v in sorted(countryCount.items(), key=lambda item: item[1], reverse=True)}
            data["homeCountry"] = homeCountry
            data["internationalDomestic"] = {"domestic":domesticCount, "international": intlCount}
            data["countryCount"] = countryCount

        def destinationDistance():
            '''https://jvectormap.com/examples/markers-world/ in JS MAP reference'''
            home = Airport(IATA=id)
            homeLat = home.lat
            homeLng = home.lng
            homeCity = home.city
            airportList = list(set([i["destinationIATA"] for i in flights if
                           i["status"] not in ["Unknown", "Canceled"]
                           and i["destinationIATA"] != '-']))
            airportList = [Airport(IATA=i) for i in airportList]
            airportDestinationlatlng = [{'latLng': [round(i.lat,2), round(i.lng,2)],
                                         "name": i.city}
                                        for i in airportList if i.lng and i.lat]
            airportDestinationlatlng.append({"latLng":[homeLat,homeLng],"name":homeCity,"style":{"r":4,"fill":"red"}})
            data["destinationWithLocation"] = airportDestinationlatlng
            airportListWithDistance = [{"name":i.name,
                                        "city": i.city,
                                        "country": i.country,
                                        "distance": calculateDistance(homeLng, homeLat, i.lng, i.lat)}
                                       for i in airportList if i.lng and i.lat]
            airportListWithDistance.sort(key=lambda x: x["distance"], reverse=True)
            data["topDistance"] = airportListWithDistance[:5]

        def fleetCategory():
            fleets = [i["aircraft"] for i in flights
                      if i["aircraft"] is not None
                      and i["status"] not in ["Unknown", "Canceled"]
                      and i["aircraft"] != "-"]
            iata = [Aircraft(IATA=i) for i in fleets if len(i) == 3]
            icao = [Aircraft(ICAO=i) for i in fleets if len(i) == 4]
            for item in iata:
                item.fetch(value=item.IATA)
            for item in icao:
                item.fetch(value=item.ICAO)
            iata = [i.Size for i in iata if i.Type is not None
                    and i.Type == "Commercial"
                    and i.Size is not None]
            icao = [i.Size for i in icao if i.Type is not None
                    and i.Type == "Commercial"
                    and i.Size is not None]
            total = iata + icao
            total = [{"type": i,
                     "count": total.count(i)}
                     for i in set(total)]
            data["fleetCategory"] = total

        def estimateTraffic():
            fleets = [i["aircraft"] for i in flights
                      if i["aircraft"] is not None
                      and i["status"] not in ["Unknown", "Canceled"]
                      and i["aircraft"] != "-"]
            iata = [Aircraft(IATA=i) for i in fleets if len(i) == 3]
            icao = [Aircraft(ICAO=i) for i in fleets if len(i) == 4]
            for item in iata:
                item.fetch(value=item.IATA)
            for item in icao:
                item.fetch(value=item.ICAO)
            iata = [float(i.Seats) for i in iata if i.Type is not None
                    and i.Type == "Commercial"
                    and i.Seats is not None]
            icao = [float(i.Seats) for i in icao if i.Type is not None
                    and i.Type == "Commercial"
                    and i.Seats is not None]
            total = int(round((sum(iata) + sum(icao)) * 0.9, 0))
            data["passengerTraffic"] = total
        
        calculateAirlineCounts()
        calculateNumOfCanceled()
        calculateTotalFlights()
        internationalDomestic()
        destinationDistance()
        fleetCategory()
        estimateTraffic()
        #return data, 200
        return Response(simplejson.dumps(data), mimetype="application/json", status=200)

class AirportWeatherApi(Resource):
    def get(self, id):
        proxy = Proxy().ip_proxies
        data = AirportSchedule(id, 0, proxy=proxy).getAirportWeather()
        if data:
            return Response(simplejson.dumps(data), mimetype="application/json", status=200)
        else:
            return {"metar": "Not Found"}, 404

class CurrentFlightApi(Resource):
    def get(self, id, status_code):
        proxy = Proxy().ip_proxies
        data = AirportSchedule(id, status_code, proxy=proxy).getCurrentData()
        return Response(simplejson.dumps(data), mimetype="application/json", status=200)

class TestApi(Resource):
    def get(self):
        random_ip = ".".join(map(str, (random.randint(0, 255)
                                       for _ in range(4))))
        items = ["linux", "unix", "win10", "macos", "aix", "zos"]
        data = {
            "processor": random.randint(1, 50),
            "ip_address": random_ip,
            "memory": random.randint(1, 50),
            "uptime": random.randint(1, 50),
            "disk_usage": random.randint(1, 50),
            "cpu_temp": random.randint(1, 50),
            "basic_info": random.choice(items)
        }
        return Response(json.dumps(data), mimetype="application/json", status=200)

class AirportApi(Resource):
    def get(self, id):
        x = Airport(IATA=id)
        airport = {"Name": x.name,
                   "IATA": x.iata,
                   "City": x.city,
                   "Country": x.country,
                   "ICAO": x.icao,
                   "Latitude":x.lat,
                   "Longitude":x.lng,
                   "CountryCode": Country(name=x.country).code}
        if x.status:
            return Response(simplejson.dumps(airport), mimetype="application/json", status=200)
        else:
            return {"error": "Please select a correct airport IATA Code!"}, 404


if __name__ == "__main__":
    FlightScheduleApi().get("IND", 1)
