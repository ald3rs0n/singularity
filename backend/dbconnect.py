import pymongo
import pandas as pd
from datetime import date,datetime
from random import randint
import os
from backend.getstockdata import getDataFromNse

DBURL = "mongodb://127.0.0.1:27017/"
client = pymongo.MongoClient(DBURL)
singularitydb = client['singularity']



# Returns a dataframe from db providing name of the stock
def getDataFromDB(stock):
    collection_name = stock.upper()
    data_collection = singularitydb[collection_name]
    query = {"Close" : {"$gt" : 520}}
    # y = data_collection.find(query) ## when query is passed returning empty in app,have to investigate
    y = data_collection.find().sort("Date",1)
    # y = data_collection.find()
    df = pd.DataFrame(y)
    if not df.empty:
        df.drop('_id',inplace=True,axis='columns')
        return df
    
    # df.to_csv('analyzed/file.csv')
    # dff = pd.read_csv('analyzed/file.csv')


# takes list of names of stocks and updates the whole database
def updateDB(watchlist,start_date):
    # start_date = date(2021,6,20)
    end_date = datetime.date(datetime.now())
    for stock in watchlist:
        try:
            df_raw = getDataFromNse(stock,start_date,end_date)
            updateCollection(df_raw)
            print("Updated "+stock)
        except Exception as e:
            print("Failed to update DB!")
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
