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
        "total size": result[1],
        "free": result[2],
        "avail": result[6],
        "use in %": round(float(result[2]) / float(result[1]) * 100, 2)
    }

def getUptime():
    response = execLinuxCom("cat /proc/uptime")
    total_mins = int(float(response.split()[0]) / 60)
    return {
        "days": int(total_mins / 24 / 60),
        "hours": int(total_mins /60 % 24),
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