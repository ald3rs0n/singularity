from datetime import datetime
from Backend.tools import Utils
from Backend.dbconnect import *
from Backend.settings import TODAY,YEAR
from Backend.dividenddata import getDividendTable,url,headers



def getData(stock,time=YEAR):
    start_date = TODAY - time
    # updateDB([stock],start_date)

    df = getDataFromDB(stock)
    if df is None:
        updateDB(stock,start_date)
        df = getDataFromDB(stock)
    if not df is None:
        date,close = (df.iloc[-1:-2:-1].get(["Date","Close"]).values[0])
        last_date = datetime.date(datetime.strptime(date,"%Y-%m-%d"))
        dt = Utils.dateCalc()
        if last_date == dt:
            return df
        else:
            # updateDB([stock],start_date)
            updateDB(stock,last_date)
            df = getDataFromDB(stock)
            return df
    return df

def getQuote(stock):
    quote = getQuoteFromDB(stock)
    if quote is None:
        updateQuote(stock)
        quote = getQuoteFromDB(stock)
    if not quote is None:
        date = quote['date']
        # quote['date'] = datetime.date(datetime.now())
        # print(f"this {quote['date']}")
        last_date = datetime.date(datetime.strptime(date,"%d-%m-%Y"))
        dt = Utils.dateCalc()
        # print(date,last_date,dt)
        if last_date >= dt:
            return quote
        else:
            updateQuote(stock)
            quote = getQuoteFromDB(stock)
            return quote
    return quote

def getUpcomingDividend():
    dt = datetime.strptime(str(Utils.dateCalc()),"%Y-%m-%d")
    query = {"ex date" : {"$gt": dt}}
    # dividend_df = getDividendFromDB(query)
    # if dividend_df.empty:
    div_list,div_table_date = getDividendTable(url,headers)
    if not div_list is None:
        updateDividendDB(div_list)
        dividend_df = getDividendFromDB(query)
        return dividend_df
    else:
        dividend_df = getDividendFromDB(query)
        return dividend_df



