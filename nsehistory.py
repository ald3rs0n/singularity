from nsepy import get_history
from datetime import datetime,date
import pandas as pd
import matplotlib.pyplot as plt
import pandas_ta as ta
from time import sleep
import numpy as np


# Goal:
# To get historical data from nse site - DONE
# extract the data and plot MACD,RSI,MA,Stochictic graph to indetify buy and sell signal
# apply machine learning to predict future market trand
# find highly flactuating stocks (flactuation > 20%)

def getStocksList():
    stocks = ['IOCL','SBIN','ZOMATO','VEDL']
    return stocks

def plotMACD():
    # data = get_history(stock,date(2021,6,10),date(2021,11,30))
    # data.to_csv(stock+'.csv')
    y = np.array([0,0])
    x = np.array([20,120])
    data = pd.read_csv('static/IOCL.csv')
    data.ta.macd(close="close",fast=12,slow=26,signal=9,append=True)
    pd.set_option("display.max_columns",None)
    dff = data.get(["Date","MACD_12_26_9","MACDs_12_26_9"])
    # plot a graph of date vs MACD
    dff.plot(x="Date")
    plt.plot(x,y)
    plt.title("MACD of IOCL")
    # plt.title("MACD of "+stock)
    plt.xlabel("Date")
    plt.ylabel("MACD")
    plt.show()

def plotRSI():
    pass

def plotMA():
    pass

def plotStochastics():
    pass

def findChartPattern():
    pass

def getSignal():
    pass


stocks = getStocksList()
# for stock in stocks:
#     print(stock)
    # plotMACD(stock)
    # sleep(5)

plotMACD()

# plt.plot()
# plt.show()

# df = pd.read_csv('/home/darkphoton/Works/singularity/NSE-stocks-04-12-2021.csv')
# print(df.drop(columns=["Purpose","Ex-dividend Date"]))