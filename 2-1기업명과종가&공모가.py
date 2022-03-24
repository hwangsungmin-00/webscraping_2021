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
    lastprice = tds[5].text
    gongmoprice=tds[2].text

    lastprice = lastprice.replace(',', '')
    lastprice=int(lastprice)

    gongmoprice = gongmoprice.replace(',', '')
    gongmoprice = int(gongmoprice)

    return {"name": name, "종가": lastprice, "공모가": gongmoprice}


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

plt.title('첫날 종가와 공모가')

x_range=np.arange(len(aaa["name"]))
plt.bar(x_range, aaa["종가"], color='cornflowerblue',width=0.25, label='첫날 종가')
plt.bar(x_range+0.3, aaa["공모가"], color='lightpink',width=0.25, label='공모가')
plt.xticks(x_range, aaa["name"], rotation=45)
plt.legend()

#배경색
ax = plt.gca()
ax.set_facecolor('white')
plt.show()