import os
import pandas as pd
import collections as col

class Day_strip(object):
    """docstring for Day_strip"""
    def __init__(self, *args):
        super(Day_strip, self).__init__()

        self.path = os.getcwd() + "/save df"
        self.list_path = os.listdir(self.path)
        self.One = pd.read_csv(self.path + "/" + self.list_path[-1], sep="|")
        self.Two = pd.read_csv(self.path + "/" + self.list_path[-2], sep="|")

        self.One = self.One.drop("Unnamed: 0", 1)
        self.Two = self.Two.drop("Unnamed: 0", 1)

    def insader(self):
        print(list(self.One.columns))
        df1 = self.One.groupby(["ID_house", "room"]).aggregate({"price_2": "mean"}).rename(
            columns={"price_2": "price-2_mean_1"})
        df2 = self.Two.groupby(["ID_house", "room"]).aggregate({"price_2": "mean"}).rename(
            columns={"price_2": "price-2_mean_1"})

        b = [list(col.Counter(self.One["ID_house"].to_list()).keys()),
              len(list(col.Counter(self.One["ID_house"].to_list()).keys()))]
        #print("\n")
        a = [list(col.Counter(self.Two["ID_house"].to_list()).keys()),
              len(list(col.Counter(self.Two["ID_house"].to_list()).keys()))]
        #print(len(a))
        c = [1 if a[0][u] in b[0] else 0 for u in range(len(a[0]))]
        #print(sum(c))

        DF = df1 - df2
        DF = DF.reset_index().rename(columns={"price-2_mean_1": "price_2_af_day"})
        #print(DF["price_2_af_day"].values)
        return DF

if __name__ == "__main__":
    Class0 = Day_strip()
    Class0.insader()
