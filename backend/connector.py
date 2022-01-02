from backend.dbconnect import *
from datetime import datetime,date, timedelta

def getData(stock):
    start_date = datetime.date(datetime.now()) - timedelta(days=45)
    # updateDB([stock],start_date)
    df = getDataFromDB(stock)
    return df