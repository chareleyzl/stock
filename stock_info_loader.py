# -*- coding:utf-8 -*-
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup

def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.text
    except:
        return ""

def getStockList(lst, stockURL):
    html = getHTMLText(stockURL)
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a')
    for i in a:
        try:
            href = i.attrs['href']
            lst.append(re.findall(r"[s][hz]\d{6}", href)[0])
        except:
            continue

def getStockInfo(lst, stockURL, fpath):
    count = 0
    for stock in lst:
        s = stock[2:]
        url = stockURL + s + "/yjbb.html"
        html = getHTMLText(url)
        try:
            if html=="":
                continue
            # 通过特定字符串定位
            pos1 = 'defjson:'
            s1 = html.find(pos1)
            h1 = html[s1:]

            pos2 = 'maketr:'
            s2 = h1.find(pos2)
            h2 = h1[:s2]

            h = h2[h2.find('['):h2.find(']') + 1]
            # 转换为list
            l = eval(h)
            # 转换为df
            df = pd.DataFrame.from_dict(l)
            df.to_csv(fpath+stock+'.csv', mode='w')
            count = count + 1
            print("\r当前进度: {:.2f}%".format(count*100/len(lst)),end="")
        except:
            count = count + 1
            print("\r当前进度: {:.2f}%".format(count*100/len(lst)),end="")
            continue

if __name__ == '__main__':
    #获取业绩信息
    stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
    stock_info_url = 'http://data.eastmoney.com/bbsj/stock'
    output_file = 'E:/data/stock_data/reports/'
    slist=[]
    getStockList(slist, stock_list_url)
    getStockInfo(slist, stock_info_url, output_file)




