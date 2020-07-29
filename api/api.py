from flask_restful import Resource
from util import *

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