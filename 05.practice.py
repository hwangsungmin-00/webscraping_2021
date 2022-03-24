import requests
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt

def crawl(url):
    data = requests.get(url)
    print(data)
    return data.content


def getStockInfo(tr):
    tds = tr.findAll("td")
    rank = tds[0].text
    name = tds[1].find("a", {"class": "tltle"}).text
    volume = tds[6].text

    return rank, name, volume


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


x=name
y1=rank
y2=volume

fig, ax1=plt.subplots()
ax2=ax1.twinx()

# plot with properties
line1=ax1.plot(np.arange(len(x)), y1, color='b', linestyle='--', marker='o')
line2=ax1.plot(np.arange(len(x)), y2, color='g', linestyle='--', marker='^')

# plot without x sorting
ax1.set_xticklabels(x)
ax1.set_ylabel('Number')
ax2.set_ylabel('Execution Time(ms)')

# set y limit
ax1.set_ylim(1, 30)
ax2.seet_ylim(0, 1000000)

# plot legend for all y axis
lines=line1+line2
labels=[l.get_label() for l in lines]
plt.legend(lines, labels, loc=2)

plt.grid(False)

fig.tight_layout()
fig.savefig('Fig.eps', format='eps', dpi=1000)
plt.show()