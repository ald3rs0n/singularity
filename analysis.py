from talib import *
import pandas as pd
from tools import StockAnalysisTools as SAT
from getdata import getData

###     Analysis:
###     Plan:
###     take every indiactor and pattern to get buy and sell signal
###     plotting signal and pattern to visalize data -- done
###     view signal details in web,beside plot and store in file/database

# Does analysis on dataframes on given indicators and retunrs list of buy and sell options
def doAnalysis(df,*args):
    output = []
    # for df in dataframes:
    for arg in args:
        if arg.upper() == "RSI":
            rsi = SAT(df).analyzeRSI()
            output.append(rsi)
        elif arg.upper() == "STOCH":
            sto = SAT(df).analyzeStochastics()
            output.append(sto)
        else:
            print("Invalid Operation : "+arg+"\r\n")
    return output

# takes list of buy and sell dataframe and writes to a csv file
def writetocsv(vals):
    for val in vals:
        try:
            val.to_csv('analyzed/'+val.at[0,'symbol']+'_'+(val.columns.values)[2]+'.csv')
        except:
            pass

# dataframes = getData()
# vals = doAnalysis(dataframes,'rsi','stoch')

# writetocsv(vals)
# for val in vals:
    # print(val)
# print(dataframes)
