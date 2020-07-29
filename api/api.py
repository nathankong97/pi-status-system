from flask_restful import Resource
from util import *
from flask import Response
import json, random



class RpiStatusApi(Resource):
    def get(self):
        data = {
            "processor": getProcessInfo(),
            "ipAddress": getIpAddress(),
            "memory": getMemoryUsage(),
            "uptime": getUptime(),
            "disk_usage": getDiskUsage(),
            "cpu_temp": getCelsius()["cpu_temperature"],
            "basic_info": getBasicInfo()
        }
        return Response(json.dumps(data), mimetype="application/json", status=200)

class TestApi(Resource):
    def get(self):
        random_ip = ".".join(map(str, (random.randint(0, 255)
                                for _ in range(4))))
        items = ["linux", "unix", "win10", "macos", "aix", "zos"]
        data = {
            "processor": random.randint(1,50),
            "ipAddress": random_ip,
            "memory": random.randint(1,50),
            "uptime": random.randint(1,50),
            "disk_usage": random.randint(1,50),
            "cpu_temp": random.randint(1,50),
            "basic_info": random.choice(items)
        }
        return Response(json.dumps(data), mimetype="application/json", status=200)