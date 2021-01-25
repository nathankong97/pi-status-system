from flask_restful import Resource
from util import *
from flask import Response
import json, simplejson
import random
from models import AirportSchedule
from db_models import Airport, Airline, Country, Aircraft, Cars
from proxy import Proxy
from db import db


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
        # data = getLocation()
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
            airlines = [i["airlineIATA"] for i in flights if
                        i["airlineIATA"] and i["airlineIATA"] != "-" and i["status"] not in ["Unknown", "Canceled"]]
            airlineDict = {}
            for i in airlines:
                if i not in airlineDict:
                    airlineDict[i] = 1
                else:
                    airlineDict[i] += 1
            airlineDict = {k: v for k, v in sorted(airlineDict.items(), key=lambda item: item[1], reverse=True)}
            airlineList = [Airline(IATA=i).name for i in list(airlineDict.keys())][:5]
            iata = list(airlineDict.keys())[:5]
            counts = list(airlineDict.values())[:5]
            data["calculateAirlineCounts"] = {"iata": iata, "airlines": airlineList, "counts": counts}

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
            data["internationalDomestic"] = {"domestic": domesticCount, "international": intlCount}
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
            airportDestinationlatlng = [{'latLng': [round(i.lat, 2), round(i.lng, 2)],
                                         "name": i.city}
                                        for i in airportList if i.lng and i.lat]
            airportDestinationlatlng.append(
                {"latLng": [homeLat, homeLng], "name": homeCity, "style": {"r": 4, "fill": "red"}})
            data["destinationWithLocation"] = airportDestinationlatlng
            airportListWithDistance = [{"name": i.name,
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
        # return data, 200
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

class AirportDetailApi(Resource):
    def get(self, id):
        proxy = Proxy().ip_proxies
        data = AirportSchedule(id, 0, proxy=proxy).getDetails()
        if data:
            return Response(simplejson.dumps(data), mimetype="application/json", status=200)
        else:
            return {"error": "Not Found"}, 404

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
                   "Latitude": x.lat,
                   "Longitude": x.lng,
                   "CountryCode": Country(name=x.country).code}
        if x.status:
            return Response(simplejson.dumps(airport), mimetype="application/json", status=200)
        else:
            return {"error": "Please select a correct airport IATA Code!"}, 404


class FlightDatesCountApi(Resource):
    def get(self):
        d = db()
        data = d.fetchall(d.COUNT_BY_DAY_QUERY)
        data_jp = d.fetchall(d.COUNT_BY_DAY_JP_QUERY)
        json_data = {"us": {
                "count": [i[0] for i in data],
                "label": [i[1].strftime('%Y-%m-%d') for i in data]},
            "japan": {
                "count": [i[0] for i in data_jp],
                "label": [i[1].strftime('%Y-%m-%d') for i in data_jp]
            }
        }
        return Response(simplejson.dumps(json_data), mimetype="application/json", status=200)


class CarsInfoApi(Resource):
    def get(self, model, zipcode):
        result = Cars(model, zipcode).fetchall()
        return Response(simplejson.dumps(result), mimetype="application/json", status=200)

class FlightNumByAirlineApi(Resource):
    def get(self, airline):
        d = db()
        data = d.fetchall(d.FLIGHT_NUM_BY_AIRLINE_QUERY.format(airline, airline))
        json_data = [{
            "flight_num": int(i[0][2:]),
            "origin": i[1],
            "origin_city": i[2],
            "origin_country": i[3],
            "dest": i[4],
            "dest_city": i[5],
            "dest_country": i[6],
            "intl": True if i[3] != i[6] else False
        } for i in data]
        return Response(simplejson.dumps(json_data), mimetype="application/json", status=200)

class AllAirportsApi(Resource):
    def get(self):
        payload = {"results": get_all_airports()}
        return Response(simplejson.dumps(payload), mimetype="application/json", status=200)

class AllianceApi(Resource):
    def get(self, id):
        data = db().fetchall(db.ALLIANCE_QUERY.format(id.upper()))
        name = [i[0] if i[0] is not None else "Others" for i in data]
        count = [i[1] for i in data]
        json_data = {
            "name": name,
            "data": count
        }
        return Response(simplejson.dumps(json_data), mimetype="application/json", status=200)

class AirportFlightPathApi(Resource):
    def get(self, id):
        data = db().fetchall(db.AIRPORT_DEST_COORDINATE_QUERY.format(id.upper()))
        lat, lng = db().fetchall(db.COORDINATE_BY_AIRPORT_QUERY.format(id.upper()))[0]
        start_lat = [lat] * len(data)
        start_lng = [lng] * len(data)
        end_lat, end_lng, count = map(list, zip(*data))
        max_count = max(count)
        json_data = {
            "start_lat": start_lat,
            "start_lng": start_lng,
            "end_lat": end_lat,
            "end_lng": end_lng,
            "count": count,
            "max_count": max_count
        }
        return Response(simplejson.dumps(json_data), mimetype="application/json", status=200)

class AirportTimeSeriesApi(Resource):
    def get(self, id):
        try:
            s = {0: "origin", 1: "dest"}
            d = db()
            d.execute("SET time_zone = '+0:00';")
            data = d.fetchall(d.TIME_SERIES_AIRPORT_QUERY.format(s[0],id.upper()))
            data2 = d.fetchall(d.TIME_SERIES_AIRPORT_QUERY.format(s[1],id.upper()))
            dep_count, dep_time = map(list, zip(*data))
            arr_count, arr_time = map(list, zip(*data2))
            json_data = {
                "origin_time": dep_time,
                "origin_count": dep_count,
                "arrival_count": arr_count,
                "arrival_time": arr_time
            }
            return Response(simplejson.dumps(json_data), mimetype="application/json", status=200)
        except:
            return {"error": "Please select a correct airport IATA Code"}, 404

class AirportPopDestinationApi(Resource):
    def get(self, id):
        pop_dest = db().fetchall(db.POP_DEST_BY_AIRPORT_QUERY.format(id.upper()))
        pop_list = [{
            "name": "{} ({})".format(i[2], i[4]),
            "city": "{}, {}".format(i[0], i[1]),
            "count": i[3],
            "carrier": i[5]
        } for i in pop_dest]
        return Response(simplejson.dumps({"data": pop_list}), mimetype="application/json", status=200)

class AirlinePopDestinationApi(Resource):
    def get(self, id):
        try:
            pop_dest = db().fetchall(db.AIRLINE_POP_AIRPORT_QUERY.format(id.upper()))
            json_data = [{
                "name": i[0],
                "iata": i[1]
            } for i in pop_dest]
            return Response(simplejson.dumps(json_data), mimetype="application/json", status=200)
        except:
            return {"error": "Please select a correct airport IATA Code"}, 404

if __name__ == "__main__":
    CarsInfoApi("20017", "46204")
