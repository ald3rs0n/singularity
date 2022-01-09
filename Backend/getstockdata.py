from nsepy import get_history   # Get historical data from NSE site
from nsetools import Nse        # Get current data from nse site
import pandas as pd
from Backend.settings import IP

# retunrs list of stocks in a dictionary
def NseStocks():
    if IP != '127.0.0.1':
        nse = Nse()
        df_dict = nse.get_stock_codes()  # returns names of stocks and code(IOCL)
        return df_dict
    else:
        print("no internet")


# returns dataframe of stocks. If offline then from file,if online then from nse site
def getDataFromNse(stock,start_date,end_date):
    if IP != '127.0.0.1':
        df = get_history(stock.upper(),start_date,end_date)
        print("Got data of "+ stock.upper() + " from server...")
        return df 
    else:
        print("No internet connection...!")   
        return


#returns list of all dataframes of stocks present in database,try to aviod this function!
# def getAllData():
#     sc = pd.read_csv("static/stocks.csv")
#     dfs = []
#     for i,v in sc.iterrows():
#         symbol =v ['SYMBOL']
#         # company_name = v['NAME OF COMPANY']
#         df = getDataFromDB(symbol)
#         try:
#             if not df.empty:
#                 dfs.append(df)
#         except AttributeError:
#             pass
#     return dfs
