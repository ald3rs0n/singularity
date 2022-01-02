from talib import *
import pandas as pd
from backend.tools import StockAnalysisTools as SAT

###     Analysis:
###     Plan:
###     take every indiactor and pattern to get buy and sell signal
###     plotting signal and pattern to visalize data -- done
###     view signal details in web,beside plot and store in file/database

# Does analysis on a single dataframe on given indicators and retunrs list of dataframe of buy and sell options
def doAnalysis(df,args):
    output = []
    pRSI = {
        'time' : 14,
        'buy' : 70,
        'sell' : 30,
        'price' : 'close', # open,close,high,low
        }
    pSTO = {
        'buy':20,
        'sell':80,
        'fastkp':5,
        'slowkp':3, 
        'slowkm':0, 
        'slowdp':3, 
        'slowdm':0
        }
    pMACD = {
        'price':'close',
        'fp':12,
        'sp':26,
        'slp':9
        }

    for arg in args:
        if arg.upper() == "RSI":
            rsi = SAT(df).analyzeRSI(pRSI)
            output.append(rsi.iloc[0:5])
        elif arg.upper() == "STOCH":
            sto = SAT(df).analyzeStochastics(pSTO)
            output.append(sto.iloc[0:5])
        elif arg.upper() == "MACD":
            macd = SAT(df).analyzeMACD(pMACD)
            output.append(macd.iloc[0:5])
        else:
            print("Invalid Operation : "+arg+"\r\n")
    return output

# Does analysis all dataframes on given indicators and retunrs list of buy and sell options
def analyzeAll(dfs,args):
    allanalysis = []
    for df in dfs:
        output = doAnalysis(df,args)
        allanalysis.append(output)
    return allanalysis


# takes list of buy and sell dataframe and writes to a csv file
def writetocsv(vals):
    for val in vals:
        try:
            val.to_csv('analyzed/'+val.at[0,'symbol']+'_'+(val.columns.values)[2]+'.csv')
        except:
            pass



# writetocsv(vals)
# for val in vals:
    # print(val)
# print(dataframes)
