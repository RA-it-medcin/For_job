from random import choice
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class Proxy_save(object):
    """docstring for Proxy_save"""
    def __init__(self, *args):
        super(Proxy_save, self).__init__()

        self.url_proxy = "https://hidemy.name/ru/proxy-list/"

        self.poxy_open_file = open("poxy.txt", encoding="utf-8").readlines()
        for i in range(len(self.poxy_open_file)):
            self.poxy_open_file[i] = self.poxy_open_file[i].split("\n")[0]
            self.poxy_open_file[i] = {"httt": "http://" + self.poxy_open_file[i]}

    def ret_proxy(self):
        proxy_get = choice(self.poxy_open_file)
        return proxy_get

    def get_html(self, proxyd, params=None):
        haders = {"User-Agent": UserAgent().random,
                  "accept": "*/*"}
        r = requests.get(self.url_proxy, headers={"User-Agent": UserAgent().random,
                                                  "accept": "*/*"}, params=params, proxies=proxyd)
        return r

    def get_poxy(self, html):
        soup = BeautifulSoup(html, "lxml")
        items = soup.find_all("div", class_="table_block")
        proxy_list = []
        for item in items:
            t = item.find("tbody").find_all("tr")
            for t2 in t:
                #print(t2)
                t3 = t2.find_all("td")
                t3_0 = t3[0].get_text(strip=True)
                t3_1 = t3[1].get_text(strip=True)
                proxy_list.append(t3_0 + ":" + t3_1)

        file = open("poxy.txt", "w", encoding="utf-8")
        for k in proxy_list:
            file.write(k + "\n")
        file.close()
        print("Poxy update.")

Class_poxy = Proxy_save()
main_poxy = Class_poxy.ret_proxy()
html_poxy = Class_poxy.get_html(main_poxy)
Class_poxy.get_poxy(html_poxy.text)