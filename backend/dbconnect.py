import pymongo
import pandas as pd
# from getdata import getData
from time import sleep
from datetime import date
from random import randint
import os

DBURL = "mongodb://127.0.0.1:27017/"
client = pymongo.MongoClient(DBURL)
singularitydb = client['singularity']

def getDataFromDB(collection_name):
    data_collection = singularitydb[collection_name]
    query = {"Close" : {"$gt" : 520}}
    # y = data_collection.find(query) ## when query is passed returning empty in app,have to investigate
    y = data_collection.find()
    df = pd.DataFrame(y)
    if not df.empty:
        df.drop('_id',inplace=True,axis='columns')
        return df
    
    # df.to_csv('analyzed/file.csv')
    # dff = pd.read_csv('analyzed/file.csv')


# Dangerous function, Calling it in application multiple times will create multiple copies of data
def saveDataToDB(df):
    # collection_name = (df[['Symbol']])[0]
    # collection_name = 'SBIN'
    # data_collection = singularitydb[collection_name]
    # data_collection = db_name[collection_name]
    # data_collection.insert_many(df.to_dict('records'))
    df.to_csv('f.csv')
    print(pd.read_csv('f.csv'))
    # dff = { "Date" : str((df.index.values))}
    # print(dff)



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
