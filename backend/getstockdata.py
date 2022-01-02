from nsepy import get_history   # Get historical data from NSE site
from nsetools import Nse        # Get current data from nse site
from datetime import datetime,date
import pandas as pd
from backend.settings import *

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

# returns dataframe of stocks. If offline then from file,if online then from nse site
def getDataFromNse(stock,start_date,end_date):
    if IP != '127.0.0.1':
        df = get_history(stock.upper(),start_date,end_date)
        print("Got data of "+ stock.upper() + " from server...")
        print(IP)
        return df 
    else:
        print("No internet connection...!")   
        return


#returns list of all dataframes of stocks present in database,try to aviod this function!
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
