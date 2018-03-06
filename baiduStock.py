'''
a spider to download baidu stock infomation.
'''
import requests 
from bs4 import BeautifulSoup
import traceback
import re
import sys
import json

def getHTMLText(url, code='utf-8'):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        print("Request Failed")

def getStockList(lst, stockURL):
    html = getHTMLText(stockURL, 'GB2312')
    soup = BeautifulSoup(html, "lxml")
    lis = soup.find_all('li')
    for li in lis:
        try:
            href = li.a['href']
            lst.append(re.search(r"[s][hz]\d{6}", href).group())
        except:
            # traceback.print_exc()
            continue

def getStockInfo(lst, stockURL, fpath):
    total_url = len(lst)
    count = 0

    data = open(fpath, 'w')
    for stock in lst:
        stockDict = {}
        stockInfo = {}
        url = stockURL + stock + ".html"
        html = getHTMLText(url)
        try:
            count += 1
            if html == "":
                continue
            soup = BeautifulSoup(html, "lxml")
            stockname_tag = soup.find_all('a', attrs={'class':'bets-name'})
            stockInfo_tag = soup.find_all('dl')
            stockname = stockname_tag[0].text.strip()
            for dl in stockInfo_tag:
                key = dl.dt.text
                val = dl.dd.text
                stockInfo[key] = val
            if not stockInfo:
                continue
            stockDict[stockname] = stockInfo
            data.write(json.dumps(stockDict, ensure_ascii=False)+'\n')
            sys.stdout.write("\r已完成%.2f%%"%(100*count/total_url))
            sys.stdout.flush()
        except:
            # traceback.print_exc()
            count += 1
            sys.stdout.write("\r已完成%.2f%%"%(100*count/total_url))
            sys.stdout.flush()
    data.close()
   print("数据写入完毕")

def main():
    stock_list_url = "http://quote.eastmoney.com/stocklist.html"
    stock_info_url = "https://gupiao.baidu.com/stock/"
    output_file = "/home/dingjunfeng/文档/BaiduStockInfo.json"
    lst = []
    getStockList(lst, stock_list_url)
    getStockInfo(lst, stock_info_url, output_file)

if __name__ == '__main__':
    main()

