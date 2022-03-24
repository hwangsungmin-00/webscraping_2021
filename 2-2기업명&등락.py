import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def crawl(url):
    data = requests.get(url)
    print(data)
    return data.content


def getStockInfo(tr):
    tds = tr.findAll("td")
    name = tds[0].text
    suic1 = tds[4].text
    suic2=tds[6].text

    suic1 = suic1.replace('%', '')
    suic1=float(suic1)

    suic2 = suic2.replace('%', '')
    suic2 = float(suic2)

    return {"name": name, "수익률1": suic1, "수익률2": suic2}


def parse(pageString):
    bsObj = BeautifulSoup(pageString, "html.parser")
    content_center_board = bsObj.find("div", {"class": "content-center-board"})
    tbody=content_center_board.find("tbody")
    trs = tbody.findAll("tr")

    stockInfos = []
    for i in range(2, 29):
        try:
            tr = trs[i]
            stockInfo = getStockInfo(tr)
            stockInfos.append(stockInfo)
        except Exception as e:
            pass
    return stockInfos


def getSiseMarketSum(page):
    url="http://iponote.co.kr/ipo/ipo6.php?&page={}".format(page)
    pageString=crawl(url)
    list=parse(pageString)
    return list

result=[]

for page in range(1, 3):
    list=getSiseMarketSum(page)
    result+=list
print(result)

aaa=pd.DataFrame(result)
print(aaa)

#한글깨짐
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False #한글 폰트 사용시 마이너스 폰트 깨짐 해결

plt.title('기업의 등락')

x_range=np.arange(len(aaa["name"]))
plt.bar(x_range, aaa["수익률1"], color='cornflowerblue', width=0.25, label='시초가 수익률1')
plt.bar(x_range+0.3, aaa["수익률2"], color='lightpink', width=0.25, label='첫날 종가 수익률2')
plt.xticks(x_range, aaa["name"], rotation=45)
plt.legend()

#배경색
ax = plt.gca()
ax.set_facecolor('white')
plt.show()