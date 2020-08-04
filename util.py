import os


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
    return conts

if __name__ == "__main__":
    getWifiPower()
