from config import user_name,password_,host_,port_,database_

import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import pandas as pd
from sqlalchemy import create_engine




class SQL_run(object):
    """docstring for SQL_run"""
    def __init__(self, *args):
        super(SQL_run, self).__init__()
        self.path = os.getcwd() + "/save df"
        self.DaFr = pd.read_csv(self.path + "/" + os.listdir(self.path)[-1], sep="|")
        self.DaFr_name = list(self.DaFr.columns)

    def BD(self,diff_house):
        try:
            # Подключение к существующей базе данных
            connection = psycopg2.connect(user=user_name, password=password_, host=host_, port=port_,
                                          database=database_)
            connection.autocommit = True
            # Курсор для выполнения операций с базой данных
            cursor = connection.cursor()
            # Распечатать сведения о PostgreSQL
            print("Информация о сервере PostgreSQL")
            print(connection.get_dsn_parameters(), "\n")
            # Выполнение SQL-запроса
            cursor.execute("SELECT version();")

            # Получить результат
            record = cursor.fetchone()
            print("Вы подключены к - ", record, "\n")

            glab = 'postgresql+psycopg2://' + user_name + ':' + password_ + "@" + host_ + ":" + port_ + "/" + database_

            print(glab)

            Engine = create_engine(glab)

            cursor.execute(
                "DROP TABLE IF EXISTS my_table , table_2"
            )



            self.DaFr.to_sql("my_table", con=Engine, schema= None)

            diff_house.to_sql("table_2", con=Engine, schema= None)

            # cursor.execute(
            #     "SELECT * FROM my_table"
            # )
            # print("Fetchone 'my-table':",cursor.fetchone())
            #
            # cursor.execute(
            #     "SELECT * FROM table_2"
            # )
            # print("Fetchone 'table_2':", cursor.fetchone())
            print("Данные занесены в {}".format(database_))
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")