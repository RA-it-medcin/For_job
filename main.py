import random
import requests
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import os
import sys
import json
import re
import datetime
import numpy as np

import pandas as pd
import traceback

url_proxy = "https://hidemy.name/ru/proxy-list/"
HOST_main_url = "https://novosibirsk.n1.ru"


class Parsing(object):
    """docstring for Parsing"""
    def __init__(self, *args):
        super(Parsing, self).__init__()
    def test_request(self, url, retry=5, proxy=None):
        try:
            response = requests.get(url=url, headers={"User-Agent": UserAgent().random,
                                                      "accept": "*/*"}, proxies=proxy)
            print(f"Status: |+| {url} {response.status_code}")

        except Exception as ex:
            time.sleep(2)
            if retry:
                print(f"[INFO] retru ={retry} => {url}")
                return Class0.test_request(url, retry=(retry - 1))
            else:
                raise
        else:
            return response

    def get_html(self, html):
        soup = BeautifulSoup(html, "lxml")
        items = soup.find_all("div", class_="table_block")
        proxy_list = []
        for item in items:
            t = item.find("tbody").find_all("tr")
            for t2 in t:
                t3 = t2.find_all("td")
                t3_0 = t3[0].get_text(strip=True)
                t3_1 = t3[1].get_text(strip=True)
                proxy_list.append({"httt": "http://" + t3_0 + ":" + t3_1})
        return proxy_list

class Parser_nov(object):
    def __init__(self, *args):
        super(Parser_nov, self).__init__()

    def get_content(self,html,new_proxy2,line_open_file):
        soup = BeautifulSoup(html, "lxml")
        items = soup.find_all("div", class_="living-list-card")
        all_peremens = []
        for item in items:
            adress = item.find("div", class_="card-title living-list-card__inner-block").get_text(strip=True).split(
                "Показать")[0].split("-к,")[1] + " , Новосибирск, Россия"
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
            #print("Конечный id:", id_house)
            room_ = item.find("div", class_="card-title living-list-card__inner-block").get_text(strip=True).split("-к,")[0]
            time.sleep(1)
            url_data = HOST_main_url + item.find("div", class_="card-title living-list-card__inner-block").find("a",class_="link").get("href")
            html_data = Class0.test_request(url_data, new_proxy2)


            def get_content2(html2, a):
                soup2 = BeautifulSoup(html2, "lxml")
                item2 = soup2.find("div", class_="card-living-content-params__col _last").find('span',
                                                                                               class_="card-living-content-params-list__value").get_text(
                    strip=True)
                item3 = soup2.find("a", class_="card-living-content-params__more-offers")
                script =  soup2.find_all("script")[25]

                print("\n-----------------------------")
                print(script)
                print(len(soup2.find_all("script")))
                print("-----------------------------\n")
                script = re.sub("undefined","0",soup2.find_all("script")[25].string[39:])
                script = script[:script.index(";var pageMeta")]
                g = script.index("new Date")
                g1 = script[g:].index(",")+g
                #print(g,g1)
                #print(script)
                script = script[:g] + "0"+ script[g1:]
                json_script = json.loads(script)
                #print(json_script) ["__INITIAL_STATE__"]["OffersSearch"]["offers"]["result"][0]["params"]["location"]
                dict_value = json.dumps(json_script["__INITIAL_STATE__"]["OfferCard"]["offerData"]["params"]["location"], indent=4, sort_keys=True)
                print("Ширина и долгота",dict_value)
                
                json_script = json.loads(dict_value)
                latitude_ = json_script["lat"]
                longitude_ = json_script["lon"]

                if item3 == None:
                    item3 = np.nan
                    mean_price_apatmen = np.nan
                else:
                    item3 = HOST_main_url + soup2.find("a", class_="card-living-content-params__more-offers").get(
                        "href")
                    html_data_all_house = Class0.test_request(item3, proxy = random.choice(Return_poxy))

                    def get_content3(html3, a):
                        print("HTM3 обработка")
                        soup3 = BeautifulSoup(html3.text, "html.parser")
                        items3 = soup3.find_all("div", class_="living-list-card")
                        mean_score = []

                        for item2 in items3:
                            room_2 = item2.find("div", class_="card-title living-list-card__inner-block").get_text(
                                strip=True).split("-к,")[0]
                            #print("Херня:", item2)
                            if a == room_2:
                                price_2_3 = float(re.sub(" ", "", item2.find("div",
                                                                             class_="living-list-card-price__item _per-sqm").get(
                                    "title").split("руб")[0]))
                                mean_score.append(price_2_3)
                            else:
                                pass
                        Mean_price_in_house = float("{:.3f}".format(np.mean(mean_score)))
                        print(Mean_price_in_house)
                        return Mean_price_in_house

                    mean_price_apatmen = get_content3(html_data_all_house, a)

                return item2, item3, mean_price_apatmen,latitude_,longitude_

            year, url_all_house, mean_price_apatmen_in_house, latitude_,longitude_ = get_content2(html_data.text, room_)

            all_peremens.append({
                    "ID_house": [id_house],
                    "room": [room_],

                    "adress": [adress],
                    "longitude": [longitude_],
                    'latitude': [latitude_],

                    "link": [url_data],

                    "price": [float("{:.2f}".format(float(re.sub(" ", "", item.find("div",
                                                                                                       class_="living-list-card-price__item _object").get(
                                            "title").split(" руб")[0]))))],

                    "price_2": [float("{:.2f}".format(float(re.sub(" ", '', item.find("div",
                                                                                                         class_="living-list-card-price__item _per-sqm").get(
                                            "title").split(" руб")[0]))))],

                    "S_2": [item.find("div",
                                                         class_="living-list-card__area living-list-card-area living-list-card__inner-block").get_text(
                                            strip=True)],

                    "high": [item.find("span", class_="living-list-card-floor__item").get_text(strip=True)],

                    "materials": [item.find('div',
                                                               class_="living-list-card__material living-list-card-material living-list-card__inner-block").get(
                                            "title")],
                    "years": [year],
                    "url_all_house": [url_all_house],
                    "Mean_price_in_apartmen": [mean_price_apatmen_in_house],

                })
        return all_peremens

if __name__ == "__main__":
        try:
            Class0 = Parsing()
            test_request_ = Class0.test_request(url_proxy)
            Return_poxy = Class0.get_html(test_request_.text)
        except Exception as ex1:
            print(f"Ошибка подключения к прокси листам.[INFO]: {ex1}")

        try:
            Class1 = Parser_nov()
            list_dict = []
            for i in range(1,2):
                if "House_id.txt" in os.listdir(os.getcwd()):
                    txt_house1 = open("House_id.txt", "r").readlines()
                    txt_house = open("House_id.txt", "a")
                else:
                    txt_house = open("House_id.txt", "w+")
                    txt_house1 = open("House_id.txt", "r").readlines()
                html_house = Class0.test_request(f"https://novosibirsk.n1.ru/kupit/kvartiry/?page={i}&limit=25",proxy = random.choice(Return_poxy))
                list_dict1 = Class1.get_content(html_house.text, random.choice(Return_poxy), txt_house1)
                list_dict += list_dict1
                txt_house.close()

            print("Формирование датафрейма")
            
            main_df = pd.DataFrame()
            for ij in range(len(list_dict)):
                df = pd.DataFrame(list_dict[ij])
                main_df = pd.concat([main_df,df],axis = 0)

            if "Data_cvs" not in os.listdir(os.getcwd()):
                os.mkdir("Data_cvs")
                path_data = os.getcwd()+"/Data_cvs"
                main_df.to_excel(path_data + "/database - " + str(datetime.date.today()) + ".xlsx")
            elif "Data_cvs" in os.listdir(os.getcwd()):
                path_data = os.getcwd()+"/Data_cvs"
                main_df.to_excel(path_data + "/database - " + str(datetime.date.today()) + ".xlsx")
                print("Сохранение датафрейма [SUCCESFULL]")






            print("Завершено. [successfull]")
        except Exception as ex2:
            print(f"Ошибка парсинга основного сайта [INFO]: {ex2}")
            print("-"*60)
            traceback.print_exc(file=sys.stdout)
            print("-"*60)
            
        





