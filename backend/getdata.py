from nsepy import get_history   # Get historical data from NSE site
from nsetools import Nse        # Get current data from nse site
from datetime import datetime,date
from numpy import append
# from backend.tools import StockAnalysisTools as Sat
import pandas as pd
from backend.dbconnect import *
# from dbconnect import *

# retunrs list of stocks. If offine then a herdcoded list,if online then list from nse site
def getStocksList(*args,status="offline"):
    if status == 'offline':
        stocks = ['IOCL','ONGC','SBIN','ZOMATO','VEDL']
        # stocks = ['ONGC']
        return stocks
    elif status == 'online':
        try:
            nse = Nse()
            stock_codes = nse.get_stock_codes()  # returns names of stocks and code(IOCL)
            all_stocks = []
            for key in stock_codes.keys():
                all_stocks.append(key)
            return all_stocks
        except:
            print("no internet")
            return list(args)
    elif status == 'manual':
        return list(args)

# returns list of dataframes of stocks. If offline then from file,if online then from nse site

def getData(stock,start_date,end_date):
    try:
        df = get_history(stock.upper(),start_date,end_date)
        # df.to_csv('static/'+stock.upper()+'.csv')
        print("Got data from server...")
        updateCollection(df) 
        # dff = getDataFromDB(stock.upper())
    except Exception as e:
        # print(e)
        print("No internet conncetion...,trying offline")   
    try:
        dff = getDataFromDB(stock.upper())
    except Exception as e:
        # print(e)
        print("No record found in database,try online...")
    return(dff)


def getFileData(stock):
    start_date = date(2021,6,20)
    end_date = datetime.date(datetime.now())
    df = getData(stock,start_date,end_date)
    # dff = getDataFromDB(stock.upper())
    # df = pd.read_csv('static/'+stock.upper()+'.csv')
    return df


def getAllData():
    sc = pd.read_csv("static/stocks.csv")
    dfs = []
    for i,v in sc.iterrows():
        symbol =v ['SYMBOL']
        # company_name = v['NAME OF COMPANY']
        df = getDataFromDB(symbol)
        try:
            if not df.empty:
                dfs.append(df)
        except AttributeError:
            pass
    return dfs

# getAllData()