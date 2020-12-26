import os, datetime
from math import radians, cos, sin, asin, sqrt
import json

def timing(f):
    from time import time
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        print('{} Elapsed time: {} Secs'.format(f.__name__, round(end-start, 4)))
        return result
    return wrapper

def execLinuxCom(command):
    response = os.popen(command).readline()
    return response

def execLinuxComs(command):
    response = os.popen(command).readlines()
    return response

def getProcessInfo():
    response = execLinuxComs("top -b -n1")
    result = response[1].split()
    return {
        "total": result[1],
        "running": result[3],
        "sleeping": result[5],
        "stopped": result[7],
        "zombie": result[9]
    }

def getIpAddress():
    response = execLinuxCom("hostname -I")
    result = response.split()
    if len(result) == 1:
        result.append("")
    return {
        "ipv4": result[0],
        "ipv6": result[1]
    }

def getMemoryUsage():
    response = execLinuxComs("free -m")
    result = response[1].split()
    return {
        "total size": int(result[1]),
        "used": int(result[2]),
        "avail": int(result[6]),
        "use in %": round(float(result[2]) / float(result[1]) * 100, 2)
    }

def getUptime():
    response = execLinuxCom("cat /proc/uptime")
    total_mins = int(float(response.split()[0]) / 60)
    return {
        "days": int(total_mins / 24 / 60),
        "hours": int(total_mins / 60 % 24),
        "minutes": total_mins % 60
    }

def getDiskUsage():
    response = execLinuxComs('df -h')
    result = response[1].split()
    return {
        "path": result[0],
        "size": result[1],
        "used": result[2],
        "avail": result[3],
        "use in %": result[4]
    }

def getCelsius():
    response = execLinuxCom("vcgencmd measure_temp")
    temp = float(response.replace("temp=", "").replace("'C\n", ""))
    return {
        "cpu_temperature": temp
    }

def getBasicInfo():
    response = execLinuxComs("cat /proc/cpuinfo")
    return {
        "hardware": response[-4].split(": ")[1].strip(),
        "serialNum": response[-2].split(": ")[1].strip(),
        "modelNnum": response[-1].split(": ")[1].strip()
    }

def getSensorsTemp():
    response = execLinuxComs("sensors")
    temp = response[2].split()[1]
    if "+" in temp:
        temp = temp.replace("+", "")
    temp = float(temp.replace("°C", ""))
    temp_f = (temp * (9 / 5)) + 32
    return {
        "temp_c": round(temp, 2),
        "temp_f": round(temp_f, 2)
    }

def getCpuInfo():
    response = execLinuxComs("lscpu")
    result = [i.split(":") for i in response]
    result = {i[0]: i[1].strip() for i in result}
    return result

def getSysInfo():
    response = execLinuxCom("uname -a")
    return response.strip()
    
def getMAC():
    response = execLinuxCom("cat /sys/class/net/wlan0/address")
    return response.strip()
    
def getDevicesOnWifi():
    out = os.popen('ip -4 neigh').read().splitlines()
    lst = []
    for i, line in enumerate(out, start=1):
        ip = line.split(' ')[0]
        h = os.popen('host {}'.format(ip)).read()
        hostname = h.split(' ')[-1]
        lst.append(ip)
    return lst
    
def getWifiName():
    response = execLinuxCom("sudo iw dev wlan0 info | grep ssid | awk '{print $2}'")
    return response.strip()
    
def getWifiPower():
    response = execLinuxCom("iwconfig wlan0 | grep -i --color quality")
    quality, signal = response.split("Signal")
    quality_num = quality.split("=")[1].split("/")[0]
    sign_num = signal.split("dBm")[0].split("=")[1].strip()
    return {
        "quality": quality_num,
        "signal": sign_num
    }

def getLastLogin():
    response = execLinuxCom("uptime --since")
    return response.strip()

def getLocation():
    import urllib.request, json
    from fake_useragent import UserAgent
    ua = UserAgent()
    response = execLinuxCom("wget -qO- http://ipecho.net/plain | xargs echo")
    public_ip = response.strip()
    url = "https://ipinfo.io/{}".format(public_ip)
    req = urllib.request.Request(url, headers = {'User-Agent': ua.random})
    r = urllib.request.urlopen(req).read()
    cont = json.loads(r.decode('utf-8'))
    return cont
	
def getSpeedTest():
    cmd = "curl -s https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py | python -"
    response = execLinuxComs(cmd)
    dl = [line for line in response if "Download" in line][0].strip()
    ul = [line for line in response if "Upload" in line][0].strip()
    return {
	    "download": dl,
	    "upload": ul
	}

def getLogFileList():
    path = "/home/pi/flights-big-data/log"
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    all_logs = []
    for file in files:
        d = {}
        d["name"] = file
        full_path = "{}/{}".format(path, file)
        d["date"] = modification_date(full_path)
        d["size"] = round(os.path.getsize(full_path) / 1024, 3)
        all_logs.append(d)
    all_logs.sort(key=lambda d: datetime.datetime.strptime(d['date'], '%Y-%m-%d %H:%M:%S'), reverse=True)
    return all_logs

def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')

def convertDateTimeToUnix(dateTime):
    return int(dateTime.timestamp())

def get(d, keys):
    if not keys or d is None:
        return d
    return get(d.get(keys[0]), keys[1:])

def pprint(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pprint(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))

def calculateDistance(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees) (In KM)
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return int(round(c * r, 2))

def remove_duplicate_nested_list(nested_list):
    return list(set(tuple(sorted(sub)) for sub in nested_list))

def convertTimeStampToUnix(dateTime):
    return int(dateTime.timestamp())

def convertUnixToTimeStamp(unixtime, tz, dst):
    if unixtime is None:
        return "-"
    if dst:
        return (datetime.datetime.utcfromtimestamp(unixtime) + datetime.timedelta(hours=float(tz) + 1)).strftime('%m/%d %H:%M')
    else:
        return (datetime.datetime.utcfromtimestamp(unixtime) + datetime.timedelta(hours=float(tz))).strftime('%m/%d %H:%M')

def convertSecondToHour(seconds):
    hour,min,sec = str(datetime.timedelta(seconds=seconds)).split(":")
    return "{0}h {1}min".format(hour,min)

def get_brand_list():
    with open("data/makes.json") as f:
        data = json.load(f)
        return data

if __name__ == "__main__":
    #from api.api import *
    #FlightScheduleApi().get("IND", 1)
    print(getLogFileList())
