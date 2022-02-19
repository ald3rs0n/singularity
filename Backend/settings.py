import socket
from datetime import date, datetime, timedelta

import dash_daq as daq
import pandas as pd

# Determines time period for showing buy sell suggestion on a watchlist
WATCHLISTPERIOD = 2


#A constant to determine to give a call to nse site or not
BOOL = False
BOOL_STOCK = False
BOOL_WATCHLIST = False
BOOL_PORTFOLIO = False




#Network handlling part: IP and PORT
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    # doesn't even have to be reachable
    s.connect(('10.255.255.255', 1))
    IP = s.getsockname()[0]
except Exception:
    IP = '127.0.0.1'
finally:
    s.close()
PORT = 7000

# daq theme settings
theme = {
    'dark' : True
    }
daq.DarkThemeProvider(theme=theme)

#stock dataframe from csv
# STDF = pd.read_csv('~/singularity/static/stocks.csv')


#Time details settings
TODAY = datetime.date(datetime.now())
DAYS = timedelta(days=5)
WEEK = timedelta(days=7)
MONTH = timedelta(days=30)
QUARTER = timedelta(days=90)
HALFYEAR = timedelta(days=180)
YEAR = timedelta(days=364)
TWOYEARS = timedelta(days=730)
FIVEYEARS = timedelta(days=1826)

# Analysis parameters settings
P_RSI = {
        'time' : 14,
        'buy' : 70,
        'sell' : 30,
        'price' : 'close', # open,close,high,low
        }
P_STO = {
    'buy':20,
    'sell':80,
    'fastkp':5,
    'slowkp':3, 
    'slowkm':0, 
    'slowdp':3, 
    'slowdm':0
    }
P_MACD = {
    'price':'close',
    'fp':12,
    'sp':26,
    'slp':9
    }
P_BB = {
    'time':5,
    'price':'close',
    'nbdevup':2,
    'nvdevdn':2,
    'matype':0
    }

