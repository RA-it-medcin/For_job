from config import *
import psycopg2
from psycopg2 import sql
import pandas as pd

connection = psycopg2.connect(user=user_name, password=password_, host=host_, port=port_,
                              database=database_)
#con.autocommit = True

with connection.cursor() as cur:
	cur.execute(
		"SELECT version();")
	print("Version: ", cur.fetchone())

	cur.execute('SELECT * FROM my_table')
	columns = []

	result = cur.fetchall()

	for desc in cur.description:
		columns.append(desc[0])

	house = pd.DataFrame(result, columns = columns)
	house = house.iloc[:,2:]
	#house.to_excel("1.xlsx")

	cur.execute("SELECT * FROM table_2")
	columns = []
	for desc in cur.description:
		columns.append(desc[0])

	result2 = cur.fetchall()

	house2 = pd.DataFrame(result2,columns = columns)
	#house2.to_excel("2.xlsx")
	print(list(house.columns))

	print()
	print(list(house2.columns))


	house2 = pd.DataFrame(data = house2.drop(["index","room"],1)).set_index("ID_house")
	house = house.set_index("ID_house")
	print(house)
	print()
	print(house2)
	DF = house2.join(house)

	print(DF)
	DF.to_excel("Вот1.xlsx")


#cur.execute(sql.SQL('CREATE DATABASE {};').format(sql.Identifier("New_db")))


connection.close()