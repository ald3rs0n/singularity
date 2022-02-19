from datetime import datetime

from Backend.tools import Utils
from Backend.dbconnect import *
from Backend.settings import TODAY,QUARTER,YEAR



def getData(stock,time=YEAR):
    start_date = TODAY - time
    # updateDB([stock],start_date)

    df = getDataFromDB(stock)
    if df is None:
        updateDB([stock],start_date)
        df = getDataFromDB(stock)
    if not df is None:
        date,close = (df.iloc[-1:-2:-1].get(["Date","Close"]).values[0])
        last_date = datetime.date(datetime.strptime(date,"%Y-%m-%d"))
        dt = Utils.dateCalc()
        if last_date == dt:
            return df
        else:
            # updateDB([stock],start_date)
            updateDB([stock],last_date)
            df = getDataFromDB(stock)
            return df
    return df
