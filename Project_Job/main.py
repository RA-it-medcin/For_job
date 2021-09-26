from Proxy_update import *
from Parser import *
from work_df import  Day_strip
from ProgreSQL_ import *
import datetime
import os


if __name__ == "__main__":
    stat_p = 0
    print("Статус обновления прокси листа: ", stat_p)
    if stat_p == 1:
        Class_poxy = Proxy_save()
        main_poxy = Class_poxy.ret_proxy()
        html_poxy = Class_poxy.get_html(main_poxy)
        Class_poxy.get_poxy(html_poxy.text)
    elif stat_p == 0:
        End_file = os.listdir(os.getcwd()+"/save df")[-1].split(" ")[-1][:-4] #+ "1"
        Day = str(datetime.date.today())
        if End_file == Day:
            def start():
                print("Запись сегодня осуществлялась")
                Class2 = Day_strip()
                diff_house = Class2.insader()
                print("Обработка закончена")
                print("Запуск БД")
                Class1 = SQL_run()
                Class1.BD(diff_house)
            start()
        else:
            print("Парсинг начался")
            Class0 = Parser()
            Data = Class0.run_parser()
            print("\n","Парсинг закончен")
            start()




