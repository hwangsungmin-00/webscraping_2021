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
    name = tds[1].find("a", {"class": "tltle"}).text
    foreign_percent = tds[9].text
    foreign_percent = foreign_percent.replace(',', '')
    foreign_percent=float(foreign_percent)

    return {"name": name, "foreign_percent": foreign_percent}


def parse(pageString):
    bsObj = BeautifulSoup(pageString, "html.parser")
    box_type_l = bsObj.find("div", {"class": "box_type_l"})
    type_2 = box_type_l.find("table", {"class": "type_2"})
    trs = type_2.findAll("tr")

    stockInfos = []
    for i in range(2, 201):
        try:
            tr = trs[i]
            stockInfo = getStockInfo(tr)
            stockInfos.append(stockInfo)
        except Exception as e:
            pass
    return stockInfos


url = "https://finance.naver.com/sise/sise_quant.nhn"
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

plt.plot(aaa["name"], aaa["foreign_percent"])
plt.title('거래량 상위에서의 외국인 비율')
plt.xticks(size=5,rotation=45)
#배경색
ax = plt.gca()
ax.set_facecolor('white')
plt.show()