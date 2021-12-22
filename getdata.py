import re
from nsepy import get_history   # Get historical data from NSE site
from nsetools import Nse        # Get current data from nse site
from datetime import datetime,date
from time import sleep
from tools import StockAnalysisTools as Sat
import pandas as pd


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
def getData(stock):
    # def getData(stock,status="offline"):
    # stocks = getStocksList(*stk,status=status)
    # dataframes = []
    # for stock in stocks:
    try:
        df = get_history(stock.upper(),date(2020,12,21),date(2021,12,21))
        df.to_csv('static/'+stock.upper()+'.csv')
        print("Got data from server...") 
        # sleep(5)
        # dataframes.append(df)
    except Exception as e:
        # print(e)
        print("No internet conncetion...,trying offline")   
        try:
            df = pd.read_csv('static/'+stock.upper()+'.csv')
            # dataframes.append(df)
        except FileNotFoundError:
            print("No file found,try online...")
    # return dataframes
    return df

# getData('bororenew','wipro','tatamotors',status='manual')

def getFileData(stock):
    # dataframes = []
    # getData(stock,status='manual')
    df = pd.read_csv('static/'+stock.upper()+'.csv')
    # dataframes.append(df)
    # return dataframes
    return df
