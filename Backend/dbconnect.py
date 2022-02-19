from datetime import datetime,date
from matplotlib.collections import Collection
import pymongo
import pandas as pd
from random import randint
import os

from Backend.getstockdata import getDataFromNse,NseStocks, getDataNseBE
from Backend.settings import TODAY

DBURL = "mongodb://127.0.0.1:27017/"
client = pymongo.MongoClient(DBURL)
singularitydb = client['singularity']




# Returns a dataframe from db providing name of the stock
def getDataFromDB(stock,query={}):
    collection_name = stock.upper()
    data_collection = singularitydb[collection_name]
    # query = {"Close" : {"$gt" : 140}}
    # query = {"Date" : {"$gt" : str(date(2021,9,15))}}
    if query is None:
        y = data_collection.find().sort("Date",1)
    else:
        y = data_collection.find(query).sort("Date",1)
    df = pd.DataFrame(y)
    if not df.empty:
        df.drop('_id',inplace=True,axis='columns')
        return df
    

# takes list of names of stocks and updates the whole database
def updateDB(watchlist,start_date):
    end_date = TODAY
    # end_date = datetime.date(datetime.now())
    for stock in watchlist:
        try:
            df_raw = getDataFromNse(stock,start_date,end_date)
            updateCollection(df_raw)
            raw_df_BE = getDataNseBE(stock,start_date,end_date)
            if not raw_df_BE is None:
                updateCollection(raw_df_BE)
                # print("Updated BE data of "+stock)
            print("Updated "+stock)
        except Exception as e:
            print("Failed to update DB!",e)
            return


# updates a collection in database. 
def updateCollection(df_raw):
    r = str(randint(500,10000))

    fname = "temp/"+r+".csv"
    df_raw.to_csv(fname)
    # print("Writing data to temp file")

    df = pd.read_csv(fname)

    if os.path.exists(fname):
        os.remove(fname)
        # print("Deleted temp file...")
    else:
        print("The file does not exist") 


    for i,v in df.iterrows():
        query = {"Date" : v['Date']}
        collection_name = (df['Symbol'])[0]
        data_collection = singularitydb[collection_name]
        y = data_collection.find_one(query)
        if y == None:
            data_collection.insert_one(v.to_dict())
            # print("Data inserted to db...Successfully!")



# returns a dataframe containing names of stocks and their symbols
def getStocksList():
    col_name = singularitydb['NSE_stocks_list']
    y = col_name.find()
    df = pd.DataFrame(y)
    return df

# function for updating stocks list in db,should be run once in a while,not regularly 
def updateStockList():
    df_dict = NseStocks()
    for symbol in df_dict.keys():
        query = {"SYMBOL" : symbol}
        collection_name = 'NSE_stocks_list'
        data_collection = singularitydb[collection_name]
        y = data_collection.find_one(query)
        if y == None:
            data = {'SYMBOL': symbol, 'NAME OF COMPANY': df_dict[symbol]}
            data_collection.insert_one(data)
            return ("Data inserted to db...Successfully! "+df_dict[symbol])


#unction to get name of a stock from its symbol
def getStockname(symbol):
    """
        It takes stock symbol as a arguement and returs name of the stock from database
        return type : string
    """
    col_name =  singularitydb['NSE_stocks_list']
    y = col_name.find_one({"SYMBOL":symbol})
    name =  y['NAME OF COMPANY']
    name = name.replace("Limited","")
    # if len(name) > 20:
    #     name = name[0:20]+"..."
    return name



# Returns a watchlist from database
def getWatchlist(name_of_watchlist):
    collection_name = 'watchlist'
    collection_db = singularitydb[collection_name]
    p = list(collection_db.find())
    for i in p:
        # i.pop('_id')
        for j in i.keys():
            if name_of_watchlist == j:
                return(i[j],i['_id'])

# Returns names of all watchlists present in database
def getWatchlistNames():
    collection_name = 'watchlist'
    collection_db = singularitydb[collection_name]
    p = list(collection_db.find())
    lst = []
    for i in p:
        i.pop('_id')
        for j in i.keys():
            lst.append(j)
    return lst

# Updates the given watchlist
def addStockToWatchlist(name_of_watchlist,stock_symbol):
    """
    This function should get watchlist name and stockname from UI stock list,
    Manually adding stocknames might cause error
    """
    collection_name = 'watchlist'
    collection_db = singularitydb[collection_name]
    watchlist,_id = getWatchlist(name_of_watchlist)
    c = watchlist.count(stock_symbol)
    if not c:
        watchlist.append(stock_symbol)
        quary = {"_id" : _id}
        data = { "$set" : {name_of_watchlist : watchlist}}
        collection_db.update_one(quary,data)
        return("watchlist "+name_of_watchlist+" updated successfully!")
    else:
        return("Failed to adding "+stock_symbol+" to "+watchlist)



def deleteStockFromWatchlist(name_of_watchlist,stock_symbol):
    watchlist,_id = getWatchlist(name_of_watchlist)
    c = watchlist.count(stock_symbol)
    if c:
        watchlist.remove(stock_symbol)
        quary = {'_id' : _id}
        data = { "$set" : {name_of_watchlist : watchlist}}
        collection_name = 'watchlist'
        collection_db = singularitydb[collection_name]
        collection_db.update_one(quary,data)
        return("Stock "+stock_symbol+" Deleted from "+name_of_watchlist)

# Deletes an existing watchlist
def deleteWatchlist(name_of_watchlist):
    collection_name = 'watchlist'
    collection_db = singularitydb[collection_name]
    watchlist,_id = getWatchlist(name_of_watchlist)
    quary = {'_id' : _id}
    collection_db.delete_one(quary)
    return ("Watchlist Deleted")

# Creates a new watchlist
def createWatchlist(name_of_watchlist,stock_name):
    name = name_of_watchlist.upper()
    lst = getWatchlistNames()
    c = lst.count(name)
    if not c:
        collection_name = 'watchlist'
        collection_db = singularitydb[collection_name]
        data = {name : [stock_name]}
        collection_db.insert_one(data)
        return("Watchlist Created")

# Untested function
def deleteCollection(stock):
    collection_name = stock.upper()
    data_collection = singularitydb[collection_name]
    data_collection.drop()
    print(collection_name+" deleted from db...Successfully!")




def getNamesFromPortfolio():
    """
     This database function returns names of stocks present in portfolio in the order of investment amount
    """
    collection_db = singularitydb['portfolio']
    q = [
            {"$project": { "stock": 1, "investment": {"$multiply": [ "$buy_price", "$quantity" ]}}},
            {"$sort":{"investment":-1}}
        ]
    pf = list(collection_db.aggregate(q))
    stocks = []
    for stock in pf:
        stocks.append(stock['stock'])
    return stocks



def getPortfiloData(stock):
    collection_db = singularitydb['portfolio']
    quary = {'stock':stock}
    z = collection_db.find_one(quary)
    return z


def updatePortfolioData(action,stock,date,price,quantity,target=0,indicator=None,stoploss=0):
    collection_db = singularitydb['portfolio']
    history = singularitydb['transactions']
    h_quary = {
                'date':date,
                'stock':stock,
                'price':price,
                'quantity':quantity,
                'target':target,
                'indicator':indicator,
                'stoploss':stoploss,
                'action':action}
    q = {'stock':stock}
    z = collection_db.find_one(q)

    if action == "BUY":
        if not z:
            quary = {
                'stock':stock,
                'date':date,
                'buy_price':price,
                'quantity':quantity,
                'target':target,
                'indicator':indicator,
                'stoploss':stoploss}
            collection_db.insert_one(quary)
            history.insert_one(h_quary)
            print(collection_db.find_one({"stock":stock}))
        else:
            id = z['_id']
            total_quantity = z['quantity']+quantity
            new_buy_price = round(((z['buy_price']*z['quantity'])+(price*quantity))/total_quantity,2)
            u_quary = {
                'buy_price':new_buy_price,
                'quantity':total_quantity,
                'target':target,
                'indicator':indicator,
                'stoploss':stoploss}
            collection_db.update_one({"_id":id},{"$set":u_quary})
            history.insert_one(h_quary)
            print(collection_db.find_one({"stock":stock}))
    elif action == "SELL" and z:
        id = z['_id']
        if z['quantity'] > quantity:
            u_quary = {
                "$inc":{"quantity":-quantity}
            }
            collection_db.update_one({"_id":id},u_quary)
            history.insert_one(h_quary)
            print(collection_db.find_one({"stock":stock}))
        elif z['quantity'] == quantity:
            collection_db.delete_one({"_id":id})
            history.insert_one(h_quary)
        else:
            return










