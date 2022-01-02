from datetime import date,datetime
from backend.analysis import doAnalysis
from terminaltables import AsciiTable
from backend.dbconnect import getDataFromDB, updateDB
# from dbconnect import getDataFromDB
from static.watchlist import *


# takes list of stocks to do analysis and prints a table on terminal
def printTable(watchlist):
    updateDB(watchlist,start_date=date(2021,12,20))
    tdate = datetime.date(datetime.now())
    # tdate = date(2021,12,29)
    data = [['\033[0;37m Date \033[0m','\033[0;37m Name \033[0m','\033[0;37m Indicator \033[0m','\033[0;37m Value \033[0m','\033[0;37m Price \033[0m','\033[0;37m Advice \033[0m']]
    for stock in watchlist:
        df = getDataFromDB(stock.upper())
        if df.empty:
            pass
        resultsdf = doAnalysis(df,['rsi','macd','stoch'])
        for rdf in resultsdf:
            for i,v in rdf.iterrows():
                if v['date'] == str(tdate):
                    y = []
                    z = v.to_list()
                    if v['adv'] == "BUY":
                        for j in z:
                            fj = "\033[0;93m {0} \033[0m".format(j)
                            y.append(fj)
                    elif v['adv'] == "SELL":
                        for j in z:
                            fj = "\033[0;36m {0} \033[0m".format(j)
                            y.append(fj)
                    # data.append(v.to_list())
                    data.append(y)
    table = AsciiTable(data)
    table.title = "Buy - Sell Suggestion"
    print(table.table)




watchlist = ['sbin','ongc','reliance','rblbank']
printTable(AUTOMOBILE)













# nse = Nse()

# sc = nse.get_stock_codes()

# with open('static/stocks.csv','w') as f:
#     w = csv.writer(f)
#     for i,v in sc.items():
#         w.writerow([i,v])
