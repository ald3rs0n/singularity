from nsepy import get_history # Get historical data from NSE site
from datetime import datetime,date
from time import sleep
from plotly.subplots import make_subplots as ms # Plotting framework
import plotly.graph_objects as go
import pandas as pd
import dash # Backend server
from dash import html,dcc
from talib import * # Technical analysis library


# Goal:
# To get historical data from nse site - DONE
# extract the data and plot MACD,RSI,MA,Stochictic graph to indetify buy and sell signal
# apply machine learning to predict future market trand
# find highly flactuating stocks (flactuation > 20%)

def getStocksList():
    stocks = ['IOCL','SBIN','ZOMATO','VEDL']
    return stocks

# df = get_history(stock,date(2021,6,10),date(2021,11,30))
df = pd.read_csv('static/IOCL.csv')

class StockAnalysisTools():
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
        output = SMA(df['Open'])
        fo = go.Scatter(x=df['Date'],y=output,name='line')
        return fo

    # This function plots Stochastics indicator along with candlestick chart of the stock
    def plotStochastics(self):
        df = self.df
        slowk, slowd = STOCH(df['High'], df['Low'], df['Close'], fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
        fa = go.Scatter(x=df['Date'],y=slowk,name='line')
        fb = go.Scatter(x=df['Date'],y=slowd,name='line')
        return fa,fb


    def findChartPattern():
        pass

    def getSignal():
        pass


stocks = getStocksList()
# for stock in stocks:
#     print(stock)
    # plotMACD(stock)
    # sleep(5)

def traceIndicators(df):
    fig = go.Figure()
    fig = ms(rows=4,cols=1)
    fig.update_layout(height=800,width=1340,template="plotly_dark",xaxis_rangeslider_visible=False)
    fig.add_trace(StockAnalysisTools(df).plotStock())
    fig.add_trace(StockAnalysisTools(df).plotSMA())
    fig.add_trace(StockAnalysisTools(df).plotRSI(),row=2,col=1)
    fa,fb = StockAnalysisTools(df).plotMACD()
    fig.add_traces([fa,fb], rows=[3,3], cols=[1,1])
    fc,fd = StockAnalysisTools(df).plotStochastics()
    fig.add_traces([fc,fd], rows=[4,4], cols=[1,1])
    return fig

fig = traceIndicators(df)

app = dash.Dash()
app.layout = html.Div([dcc.Graph(figure=fig)])
app.run_server(debug=True)
