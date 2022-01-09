from Backend.tools import StockAnalysisTools as SAT
from Backend.dbconnect import getDataFromDB
from terminaltables import AsciiTable
from static.watchlist import *

#For testing advice on a single stock,retuns profit or loss statement
def adviceTest(advdf):
    initmoney = 5000
    startmoney = 5000
    endmoney = 5000
    currentmoney = 0
    currentstocks = 0
    count = 0
    for i,v in advdf.iterrows():
        count += 1
        # print("Round "+str(count))
        # print(v['date'],v['adv'],v['price'])
        if v['adv'] == "BUY":
            if initmoney > v['price']:
                currentstocks = int(initmoney/v['price'])
                currentmoney = int(initmoney - (currentstocks*v['price']))
                initmoney = 0
                endmoney = currentmoney + (currentstocks*v['price'])
                # print("Buying: Price  CurrStk CurrMon IniMon")
                # print("Buying: ",v['price'],currentstocks,currentmoney)
            elif currentmoney > v['price']:
                currentstocks = int(currentmoney/v['price'])
                currentmoney = int(currentmoney - (currentstocks*v['price']))
                endmoney = currentmoney + (currentstocks*v['price'])
                # print("Buying: ",v['price'],currentstocks,currentmoney)
        elif v['adv'] == "SELL" and currentstocks > 0:
            currentmoney += int(currentstocks*v['price'])
            currentstocks = 0
            # print("Selling: Price  CurrStk CurrMon IniMon")
            endmoney = currentmoney + (currentstocks*v['price'])
            # print("Selling: ",v['price'],currentstocks,currentmoney)
    ret = int(((endmoney-startmoney)/startmoney)*100)
    if ret > 0:
        return("Profit :\033[0;36m "+str(ret)+" %\033[0m")
    elif ret < 0:
        return("Loss :\033[0;33m "+str(ret)+" %\033[0m")
    elif ret == 0:
        return("No Trade :"+str(ret)+" %")



#For testing on a watchlist and prints a table on terminal
def testAdvices(watchlist):
    a = [['NAME',"MACD",'RSI',"STOCH"]]
    for stock in watchlist:
        b  = []
        b.append(stock.upper())
        try:
            df = getDataFromDB(stock)
            sat = SAT(df)
            x = sat.analyzeMACD()
            y = sat.analyzeRSI()
            z = sat.analyzeStochastics()
            b.append(adviceTest(x.iloc[::-1]))
            b.append(adviceTest(y.iloc[::-1]))
            b.append(adviceTest(z.iloc[::-1]))
        except :
            pass
        a.append(b)
    table = AsciiTable(a)
    table.title = "Profit Table"
    print(table.table)


testAdvices(FMCG)