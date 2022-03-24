import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import plotly
import plotly.graph_objects as go
import plotly.express as px

def crawl(url):
    data = requests.get(url)
    print(data)
    return data.content


def getStockInfo(tr):
    tds = tr.findAll("td")
    rank = tds[0].text
    name = tds[1].find("a", {"class": "tltle"}).text
    volume = tds[6].text

    volume = volume.replace(',', '')
    volume=int(volume)

    return {"rank": rank, "name": name, "volume": volume}


def parse(pageString):
    bsObj = BeautifulSoup(pageString, "html.parser")
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
    return stockInfos


url = "https://finance.naver.com/sise/lastsearch2.nhn"
pageString = crawl(url)
list = parse(pageString)

result = []
result += list
print(result)

aaa=pd.DataFrame(result)
print(aaa)

#한글깨짐
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False #한글 폰트 사용시 마이너스 폰트 깨짐 해결

plt.plot(aaa["name"], aaa["volume"])
plt.title('항목별 거래량')
#배경색
ax = plt.gca() 
ax.set_facecolor('black')
plt.show()