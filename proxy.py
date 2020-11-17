import requests
import lxml.html
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random, csv, time

class Proxy:
    def __init__(self):
        self.test_url = "https://api.flightradar24.com/common/v1/airport.json?code=ind"
        #self.ua = UserAgent(verify_ssl=False, use_cache_server=False)
        self.ip_proxies = []

        self.get_ip_proxies()
        self.get_ip_proxies_intl()

    def get_ip_proxies(self):
        url = 'http://www.nimadaili.com/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4098.3 Safari/537.36'}
        req = requests.get(url, headers=headers).content.decode()
        req_1 = lxml.html.fromstring(req)
        Ip = req_1.xpath('//tbody[@style="background: #fff;"]/tr/td/text()')
        self.ip_proxies.extend([elem for elem in Ip if ":" in elem and "." in elem])

    def get_ip_proxies_intl(self):
        with open('/home/pi/pi-status-system/ip_addresses/ip_address_01.txt', "r") as f:
            result = [i.replace("\t", ":").strip() for i in f.readlines()]
            self.ip_proxies.extend(result)
            #print(result)
            #self.ip_proxies = ["https://{}:{}".format(each["ï»¿IP Address"], each["Port"]) for each in result]

    def check_if_ip_valid(self):
        session = requests.Session()
        for ip in self.ip_proxies:
            proxy = {'http': ip}
            HEADER = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
            }
            try:
                s = session.get(self.test_url, timeout=8, proxies=proxy, headers=HEADER)
            except Exception as e:
                print(e)
                self.ip_proxies.remove(ip)
                continue
            tree = lxml.html.fromstring(s.content)
            title = tree.findtext('.//title')
            status = s.status_code
            #error = tree.xpath("//p[contains(text(),'It looks like our usage analysis algorithms')]")
            if status != 200:
                print(ip, status, title, "fail")
            else:
                print(ip, status, title, "pass")
            time.sleep(2)

if __name__ == "__main__":
    p = Proxy()
    p.check_if_ip_valid()
    #p.get_ip_proxies_intl()
    #print(p.ip_proxies)