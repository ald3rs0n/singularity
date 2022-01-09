from Backend.dbconnect import *
from Backend.settings import TODAY,QUARTER,YEAR


def getData(stock,bool,time=YEAR):
    start_date = TODAY - time
    if bool:
        updateDB([stock],start_date)
    df = getDataFromDB(stock)
    return df