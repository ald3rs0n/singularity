import pandas_ta as ta
import plotly.express as px
from plotly.subplots import make_subplots as ms
import plotly.graph_objects as go
import pandas as pd
import dash
from dash import html,dcc
from talib import *
import numpy


fig = go.Figure()
df = pd.read_csv('static/IOCL.csv')

def plotMACD(df):
    # fig = px.line(data,x=data['Date'],y=data['Open'])
    macd, macdsignal, macdhist = MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    dx = go.Scatter(x=df['Date'],y=macd,name='line')
    dy= go.Scatter(x=df['Date'],y=macdsignal,name='line')
    # fig.show()
    return dx,dy

# fig.update_layout(height=1000,width=1300,template="plotly_dark",xaxis_rangeslider_visible=False)

def plotStock(df):
    fig = go.Candlestick(x=df['Date'],
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'])
    return fig



def plotSMA(df):
    output = SMA(df['Open'])
    fig = go.Scatter(x=df['Date'],y=output,name='line')
    return fig

fig = ms(rows=2,cols=1)
fig.update_layout(height=1000,width=1300,template="plotly_dark",xaxis_rangeslider_visible=False)
fig.add_trace(plotStock(df))
fig.add_trace(plotSMA(df))
fig.add_traces([plotMACD(df)[0],plotMACD(df)[1]], rows=[2,2], cols=[1,1])


app = dash.Dash()
app.layout = html.Div([dcc.Graph(figure=fig)])
app.run_server(debug=True)
