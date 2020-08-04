from flask_restful import Resource
from util import *
from flask import Response
import json, random



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
        #return Response(json.dumps(data), mimetype="application/json", status=200)
        pass

class TestApi(Resource):
    def get(self):
        random_ip = ".".join(map(str, (random.randint(0, 255)
                                for _ in range(4))))
        items = ["linux", "unix", "win10", "macos", "aix", "zos"]
        data = {
            "processor": random.randint(1,50),
            "ip_address": random_ip,
            "memory": random.randint(1,50),
            "uptime": random.randint(1,50),
            "disk_usage": random.randint(1,50),
            "cpu_temp": random.randint(1,50),
            "basic_info": random.choice(items)
        }
        return Response(json.dumps(data), mimetype="application/json", status=200)