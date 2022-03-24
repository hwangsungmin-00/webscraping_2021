import requests
from bs4 import BeautifulSoup


def crawl(url):
    data = requests.get(url)
    print(data)
    return data.content


def getStockInfo(tr):
    tds = tr.findAll("td")
    rank = tds[0].text
    name = tds[1].find("a", {"class": "tltle"}).text
    volume = tds[6].text

    return {"rank": rank, "name": name, "volume": volume}


def parse(pageString):
    bsObj = BeautifulSoup(pageString)
    box_type_l = bsObj.find("div", {"class": "box_type_l"})
    type_5 = box_type_l.find("table", {"class": "type_5"})
    trs = type_5.findAll("tr")

    stockInfos = []
    for i in range(2, 51):
        try:
            tr = trs[i]
            stockInfo = getStockInfo(tr)
            stockInfos.append(stockInfo)
        except Exception as e:
            pass
    print(stockInfos)
    return []


url = "https://finance.naver.com/sise/lastsearch2.nhn"
pageString = crawl(url)
list = parse(pageString)

result = []
result += list
print(result)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.DataFrame(np.random.randn(30, 3), index=dates, columns=list('ABCD'))
df=pd.DataFrame(result)
print(df)