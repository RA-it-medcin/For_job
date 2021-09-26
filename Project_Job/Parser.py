import pandas as pd
import numpy as np
import os
import requests
import time
from fake_useragent import UserAgent
import re
import datetime
import io
import random
from random import choice
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim

class Parser(object):

    def __init__(self, *args):
        super(Parser, self).__init__()
        self.url = "https://novosibirsk.n1.ru/kupit/kvartiry/?page="
        self.HOST = "https://novosibirsk.n1.ru"
        self.poxy_open_file = io.open("poxy.txt", encoding="utf-8").readlines()
        for i in range(len(self.poxy_open_file)):
            self.poxy_open_file[i] = self.poxy_open_file[i].split("\n")[0]
            self.poxy_open_file[i] = {"httt": "http://" + self.poxy_open_file[i]}
        self.main_df = pd.DataFrame()

    def run_parser(self):
        def ret_proxy():
            proxy_get = choice(self.poxy_open_file)
            return proxy_get

        def get_html(url, proxyd, params=None):
            haders = {"User-Agent": UserAgent().random,
                      "accept": "*/*"}
            r = requests.get(url, headers=haders, params=params, proxies=proxyd)
            print("User-Agent",haders,"Proxy: ",proxyd)
            return r

        def get_content(html, poxy2, line_open_file):
            soup = BeautifulSoup(html, "lxml")
            items = soup.find_all("div", class_="living-list-card")
            # print(items[0])
            # sys.exit()

            bukva = []

            for item in items:
                adress = item.find("div", class_="card-title living-list-card__inner-block").get_text(strip=True).split(
                    "Показать")[0].split("-к,")[1] + " , Новосибирск, Россия"
                print(adress)
                geolocator = Nominatim(user_agent=UserAgent().random)
                location = geolocator.geocode(adress)

                if location == None:
                    location = geolocator.geocode("Новосибирск, Россия")
                    loc_true = False
                else:
                    location = location
                    loc_true = True
                    adress = location.address

                while True:
                    id_house = float(random.randint(10000, 9999999))
                    ggg = adress + "\n"
                    print("Длина существующих домов в БД: ", len(line_open_file))
                    print("Начальный ID", id_house)
                    if len(line_open_file) == 0:
                        txt_house.write(str(id_house) + " | " + adress + "\n")
                        line_open_file.append(str(id_house) + " | " + adress + "\n")
                        continue
                    if ggg not in [line_open_file[u].split(" | ")[1] for u in range(len(line_open_file))]:
                        txt_house.write(str(id_house) + " | " + adress + "\n")
                        line_open_file.append(str(id_house) + " | " + adress + "\n")
                        print("Не в списке")
                        break
                    elif ggg in [line_open_file[u].split(" | ")[1] for u in range(len(line_open_file))]:
                        id_house_index = [line_open_file[u].split(" | ")[1] for u in range(len(line_open_file))].index(
                            ggg)
                        id_house = float(line_open_file[id_house_index].split(" | ")[0])
                        print("В списке", id_house)
                        break
                print("Конечный id:", id_house)
                # sys.exit()
                room_ = item.find("div", class_="card-title living-list-card__inner-block").get_text(strip=True).split("-к,")[0]
                print(location.address)
                time.sleep(1)

                def get_content2(html2, a):
                    soup2 = BeautifulSoup(html2, "lxml")
                    item2 = soup2.find("div", class_="card-living-content-params__col _last").find('span',
                                                                                                   class_="card-living-content-params-list__value").get_text(
                        strip=True)
                    item3 = soup2.find("a", class_="card-living-content-params__more-offers")

                    parsed_html = BeautifulSoup(html2, features="html.parser")
                    item4 = parsed_html.find_all("script")
                    for ite in item4:
                        print(ite.text.strip())
                    
                    

                    sys.exit()
                    if item3 == None:
                        item3 = np.nan
                        mean_price_apatmen = np.nan
                    else:
                        item3 = self.HOST + soup2.find("a", class_="card-living-content-params__more-offers").get(
                            "href")

                        html_data_all_house = get_html(item3, poxy2)

                        def get_content3(html3, a):
                            soup3 = BeautifulSoup(html, "lxml")
                            items3 = soup3.find_all("div", class_="living-list-card")
                            mean_score = []
                            for item2 in items3:
                                room_2 = item2.find("div", class_="card-title living-list-card__inner-block").get_text(
                                    strip=True).split("-к,")[0]
                                if a == room_2:
                                    price_2_3 = float(re.sub(" ", "", item2.find("div",
                                                                                 class_="living-list-card-price__item _per-sqm").get(
                                        "title").split("руб")[0]))
                                    mean_score.append(price_2_3)
                                else:
                                    pass
                            Mean_price_in_house = float("{:.3f}".format(np.mean(mean_score)))
                            return Mean_price_in_house

                        mean_price_apatmen = get_content3(html_data_all_house, a)

                    return item2, item3, mean_price_apatmen

                url_data = self.HOST + item.find("div", class_="card-title living-list-card__inner-block").find("a",class_="link").get("href")

                html_data = get_html(url_data, poxy2)

                year, url_all_house, mean_price_apatmen_in_house = get_content2(html_data.text, room_)

                bukva.append({
                    "ID_house": id_house,
                    "room": room_,

                    "adress": adress,
                    "True/False loc": loc_true,
                    "longitude": location.longitude,
                    'latitude': location.latitude,

                    "link": url_data,

                    "price": float("{:.2f}".format(float(re.sub(" ", "", item.find("div",
                                                                                   class_="living-list-card-price__item _object").get(
                        "title").split(" руб")[0])))),

                    "price_2": float("{:.2f}".format(float(re.sub(" ", '', item.find("div",
                                                                                     class_="living-list-card-price__item _per-sqm").get(
                        "title").split(" руб")[0])))),

                    "S_2": item.find("div",
                                     class_="living-list-card__area living-list-card-area living-list-card__inner-block").get_text(
                        strip=True),

                    "high": item.find("span", class_="living-list-card-floor__item").get_text(strip=True),

                    "materials": item.find('div',
                                           class_="living-list-card__material living-list-card-material living-list-card__inner-block").get(
                        "title"),
                    "years": year,
                    "url_all_house": url_all_house,
                    "Mean_price_in_apartmen": mean_price_apatmen_in_house,

                })

                print(bukva[items.index(item)])

            return bukva

        list_dict = []
        for H in range(0, 10):
            if "House_id.txt" in os.listdir(os.getcwd()):
                txt_house1 = open("House_id.txt", "r").readlines()
                txt_house = open("House_id.txt", "a")
            else:
                txt_house = open("House_id.txt", "w+")
                txt_house1 = open("House_id.txt", "r").readlines()
            new_proxy2 = ret_proxy()
            html = get_html(self.url + str(H + 1), new_proxy2)
            list_dict1 = get_content(html.text, new_proxy2, txt_house1)
            list_dict += list_dict1
            txt_house.close()

        path = os.getcwd() + "/save df"

        for i in range(len(list_dict)):
            df = pd.DataFrame([list_dict[i]])
            self.main_df = pd.concat([self.main_df, df], 0)

        self.main_df.to_csv(path + "/database - " + str(datetime.date.today()) + ".csv", sep="|")

        return self.main_df

CLASS = Parser()
CLASS.run_parser()

