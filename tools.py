from datetime import datetime,date
from time import sleep
import pandas as pd
from talib import * # Technical analysis library
import plotly.graph_objects as go


# df = pd.read_csv('static/IOCL.csv')


class StockAnalysisTools():
    def __init__(self,dataframe):
        self.df = dataframe
        self.symbol = self.df.get("Symbol")[0]

    # Does RSI buy and sell analysis and returns a pandas dataframe
    def analyzeRSI(self):
        df = self.df
        real = RSI(df['Close'], timeperiod=14)
        data = {
        'date' : df['Date'],
        'RSI' : real,
        'price' : df['Close']
        }
        dff = pd.DataFrame(data)
        dff.dropna(inplace=True)
        output = {'date' : [],'symbol':[],'RSI' : [],'price' : [],'adv' : []}
        for index,row in dff.iterrows():
            if row['RSI'] >= 70 :
                output['date'].append(row['date'])
                output['symbol'].append(self.symbol)
                output['RSI'].append(row['RSI'])
                output['price'].append(row['price'])
                output['adv'].append("SELL")
                # sell.append("{3} Sell @ {2} on {1} ; RSI:{0} \r\n".format(row['RSI'],row['date'],row['price'],self.symbol))
            elif row['RSI'] <= 30 :
                output['date'].append(row['date'])
                output['symbol'].append(self.symbol)
                output['RSI'].append(row['RSI'])
                output['price'].append(row['price'])
                output['adv'].append("BUY")
                # buy.append("Buy @ {2} on {1} ; RSI:{0} \r\n".format(row['RSI'],row['date'],row['price']))
        return (pd.DataFrame(output))

    # Does Stochstic buy and sell analysis and returns a pandas dataframe
    def analyzeStochastics(self):
        df = self.df
        slowk, slowd = STOCH(df['High'], df['Low'], df['Close'], fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
        data = {
            'date' : df['Date'],
            'slowk' : slowk,
            'slowd' : slowd,
            'price' : df['Close']
            }
        dff = pd.DataFrame(data)
        dff.dropna(inplace=True)
        output = {'date' : [],'symbol':[],'STO' : [],'price' : [],'adv' : []}
        for index,row in dff.iterrows():
            if row['slowk'] >= 80 and row['slowd'] >= 80:
             output['date'].append(row['date'])
             output['symbol'].append(self.symbol)
             output['STO'].append(row['slowd'])
             output['price'].append(row['price'])
             output['adv'].append("SELL")
                # sell.append("Date: {0},price: {1} sell ,stochastic \r\n".format(row['date'],row['price']))
            elif row['slowk'] <= 20 and row['slowd'] <= 20:
                 output['date'].append(row['date'])
                 output['symbol'].append(self.symbol)
                 output['STO'].append(row['slowd'])
                 output['price'].append(row['price'])
                 output['adv'].append("BUY")
                # buy.append("Date: {0},price: {1} buy ,stochastic \r\n".format(row['date'],row['price']))
        return (pd.DataFrame(output))

    def analyzeMACD(self):
        print("LOL")

class VisualizationTools():
    def __init__(self,dataframe):
        self.df = dataframe

    #This function plots the candlestick chart of a stock
    def plotStock(self):
        df =  self.df
        fo = go.Candlestick(x=df['Date'],
                        open=df['Open'],
                        high=df['High'],
                        low=df['Low'],
                        close=df['Close'])
        return fo

    # This function plots MACD chart along with candlestick chart of the stock
    def plotMACD(self):
        # fig = px.line(data,x=data['Date'],y=data['Open'])
        df = self.df
        macd, macdsignal, macdhist = MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
        # macd.dropna(inplace=True)
        # macdsignal.dropna(inplace=True)
        fa = go.Scatter(x=df['Date'],y=macd,name='line')
        fb = go.Scatter(x=df['Date'],y=macdsignal,name='line')
        return fa,fb

    # This function plots RSI chart
    def plotRSI(self):
        df = self.df
        real = RSI(df['Close'], timeperiod=14)
        fo = go.Scatter(x=df['Date'],y=real,name='line')
        return fo

    # This function plots SMA chart along with candlestick chart of the stock
    def plotSMA(self):
        df = self.df
        output = SMA(df['Open'], timeperiod=50)
        fo = go.Scatter(x=df['Date'],y=output,name='line')
        return fo

    # This function plots EMA chart along with candlestick chart of the stock
    def plotEMA(self):
        df = self.df
        real = EMA(df['Close'], timeperiod=30)
        fo = go.Scatter(x=df['Date'],y=real,name='line')
        return fo
    
    # This function plots Stochastics indicator along with candlestick chart of the stock
    def plotStochastics(self):
        df = self.df
        slowk, slowd = STOCH(df['High'], df['Low'], df['Close'], fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
        fa = go.Scatter(x=df['Date'],y=slowk,name='line')
        fb = go.Scatter(x=df['Date'],y=slowd,name='line')
        return fa,fb

    # This function plots Bollinger Bands
    def plotBB(self):
        df = self.df
        upperband, middleband, lowerband = BBANDS(df['Close'], timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
        ub = go.Scatter(x=df['Date'],y=upperband,name='line')
        mb = go.Scatter(x=df['Date'],y=middleband,name='line')
        lb = go.Scatter(x=df['Date'],y=lowerband,name='line')
        return ub,mb,lb

    def findChartPattern():
        pass