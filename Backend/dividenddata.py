# https://www.moneycontrol.com/stocks/marketinfo/dividends_declared/index.php?sel_year=2022


import requests
import html_to_json
from bs4 import BeautifulSoup
from Backend.settings import getIP


year = 2022
url = f"https://www.moneycontrol.com/stocks/marketinfo/dividends_declared/index.php?sel_year={year}"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}
def getDividendTable(url,headers):
    IP = getIP()
    if IP != '127.0.0.1':
        r = requests.get(url=url,headers=headers)
        div_table_date = r.headers['Date']
        soup = BeautifulSoup(r.content,'html.parser')
        s = soup.find('table',class_= 'dvdtbl')
        print("Requesting MoneyControl...!")
        json_ = html_to_json.convert_tables(str(s))
        # print(json_)
        jso_ = json_[0]
        jso_.pop(0)
        jso_.pop(0)
        return jso_,div_table_date
    else:
        print("No internet connection!")
        return

# div = getDividendTable(url,headers)
# updateDividendDB(div)

# dt = datetime.strptime(str(Utils.dateCalc()),"%Y-%m-%d")

# query = {"ex date" : {"$gte": dt}}
# data = getDividendFromDB(query)
# print(data)
