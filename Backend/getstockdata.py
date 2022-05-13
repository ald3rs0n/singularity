from nsetools import Nse        # Get current data from nse site
from nsepy import get_history   # Get historical data from NSE site
from Backend.settings import getIP
from datetime import datetime,date

# retunrs list of stocks in a dictionary
def NseStocks():
    IP = getIP()
    if IP != '127.0.0.1':
        nse = Nse()
        df_dict = nse.get_stock_codes()  # returns names of stocks and code(IOCL)
        return df_dict
    else:
        print("no internet")


# returns dataframe of stocks
def getDataFromNse(stock,start_date,end_date):
    IP = getIP()
    if IP != '127.0.0.1':
        df = get_history(stock.upper(),start_date,end_date)
        # print("Got data of "+ stock.upper() + " from server...")
        return df 
    else:
        print("No internet connection...!")   
        return



# returns dataframe of stocks where series=BE
def getDataNseBE(stock,start_date,end_date):
    IP = getIP()
    if IP != '127.0.0.1':
        df = get_history(stock.upper(),start_date,end_date,series='BE')
        # print("Got BE data of "+ stock.upper() + " from server...")
        return df 
    else:
        print("No internet connection...!")   
        return

def getNseQuote(stock_symbol):
    IP = getIP()
    if IP != '127.0.0.1':
        nse = Nse()
        stock_dict = nse.get_quote(stock_symbol)
        stock_dict['date'] = datetime.date(datetime.now()).strftime("%d-%m-%Y")
        print(f"from web {stock_dict['date']}:{stock_dict['symbol']}")
        return stock_dict 
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
