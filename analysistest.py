from Backend.tools import StockAnalysisTools as SAT
from Backend.dbconnect import getDataFromDB
from terminaltables import AsciiTable

#For testing advice on a single stock,retuns profit or loss statement
def adviceTest(advdf):
    startmoney = 5000
    currentmoney = 5000
    endmoney = 5000
    currentstocks = 0
    buy  = 0 
    for i,v in advdf.iterrows():
        if v['adv'] == "BUY" and currentmoney > v['price']:
                recentstocks = int(currentmoney/v['price'])
                currentstocks += recentstocks
                currentmoney = int(currentmoney - (recentstocks*v['price']))
                endmoney = currentmoney + (currentstocks*v['price'])
                buy = v['price']
                print("Buying: ",v['price'],currentstocks,currentmoney,v['date'])
        elif v['adv'] == "SELL" and currentstocks > 0 and v['price'] > buy:
                if int(currentstocks*v['price']) > startmoney:
                    currentmoney += int(currentstocks*v['price'])
                    currentstocks = 0
                # print("Selling: Price  CurrStk CurrMon Date")
                    endmoney = currentmoney
                    print("Selling: ",v['price'],currentstocks,currentmoney,v['date'])
    if currentstocks == 0:
        ret = int(((endmoney-startmoney)/startmoney)*100)
        if ret > 0:
            return("Profit :\033[0;36m "+str(ret)+" %\033[0m")
        elif ret < 0:
            return("Loss :\033[0;33m "+str(ret)+" %\033[0m")
        elif ret == 0:
            return("No Trade :"+str(ret)+" %")
    else:
        money = currentmoney + (currentstocks*buy)
        ret = int(((money-startmoney)/startmoney)*100)
        return("Expected Return :"+str(ret)+" %")
        

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


# testAdvices()