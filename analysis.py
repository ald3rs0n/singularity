from talib import *
import pandas as pd


###     Analysis:
###     Plan:
###     take every indiactor and pattern to get buy and sell signal
###     plotting signal and pattern to visalize data -- done
###     view signal details in web,beside plot and store in file/database

df = pd.read_csv('static/IOCL.csv')
macd, macdsignal, macdhist = MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)

real = RSI(df['Close'], timeperiod=14)



data = {
    'date' : df['Date'],
    'RSI' : real
    }

dff = pd.DataFrame(data)
dff.dropna(inplace=True)

for index,row in dff.iterrows():
    if row['RSI'] >= 70 :
        print("{0} Sell {1} \r\n".format(row['RSI'],row['date']))

# print(dff.to_string())
# print(type(dff))

# print(macdsignal.to_string())