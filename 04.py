import requests
import matplotlib.pyplot as plt
import numpy as np
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



plt.style.use('default')
plt.rcParams['figure.figsize'] = (4, 3)
plt.rcParams['font.size'] = 12

x = np.arange(0, 3)
y1 = x+1
y2 = -x - 1

fig, ax1 = plt.subplots()
ax1.plot(name, rank, color='green')

ax2 = ax1.twinx()
ax2.plot(name, volume, color='deeppink')

plt.show()