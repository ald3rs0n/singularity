from datetime import datetime,date
import pandas as pd
from talib import * # Technical analysis library
import plotly.graph_objects as go
import plotly.express as px


# df = pd.read_csv('static/IOCL.csv')


class StockAnalysisTools():
    def __init__(self,dataframe):
        self.df = dataframe
        self.symbol = self.df.get("Symbol")[0]

    # Does RSI buy and sell analysis and returns a pandas dataframe
    def analyzeRSI(self,pRSI = {'time' : 14,'buy' : 70,'sell' : 30,'price' : 'Close'}):
        df = self.df
        real = RSI(df[pRSI['price'].capitalize()], timeperiod=pRSI['time'])
        data = {
            'date' : df['Date'],
            'RSI' : round(real,2),
            'price' : df['Close']
        }
        dff = pd.DataFrame(data)
        dff.dropna(inplace=True)
        output = {'date' : [],'symbol':[],'ind' : 'RSI','RSI' : [],'price' : [],'adv' : []}
        for index,row in dff.iterrows():
            if row['RSI'] >= pRSI['buy'] :
                output['date'].append(row['date'])
                output['symbol'].append(self.symbol)
                output['RSI'].append(row['RSI'])
                output['price'].append(row['price'])
                output['adv'].append("SELL")
                # sell.append("{3} Sell @ {2} on {1} ; RSI:{0} \r\n".format(row['RSI'],row['date'],row['price'],self.symbol))
            elif row['RSI'] <= pRSI['sell'] :
                output['date'].append(row['date'])
                output['symbol'].append(self.symbol)
                output['RSI'].append(row['RSI'])
                output['price'].append(row['price'])
                output['adv'].append("BUY")
                # buy.append("Buy @ {2} on {1} ; RSI:{0} \r\n".format(row['RSI'],row['date'],row['price']))
        return (pd.DataFrame(output).iloc[::-1])
        # return (pd.DataFrame(output))

    # Does Stochstic buy and sell analysis and returns a pandas dataframe
    def analyzeStochastics(self,pSTO={'buy':20,'sell':80,'fastkp':5, 'slowkp':3, 'slowkm':0, 'slowdp':3, 'slowdm':0}):
        df = self.df
        slowk, slowd = STOCH(df['High'], df['Low'], df['Close'], fastk_period=pSTO['fastkp'], slowk_period=pSTO['slowkp'], slowk_matype=pSTO['slowkm'], slowd_period=pSTO['slowdp'], slowd_matype=pSTO['slowdm'])
        data = {
            'date' : df['Date'],
            'slowk' : round(slowk,2),
            'slowd' : round(slowd,2),
            'price' : df['Close']
            }
        dff = pd.DataFrame(data)
        dff.dropna(inplace=True)
        output = {'date' : [],'symbol':[],'ind' : 'STOCH','STO' : [],'price' : [],'adv' : []}
        for index,row in dff.iterrows():
            if row['slowk'] >= pSTO['sell'] and row['slowd'] >= pSTO['sell']:
             output['date'].append(row['date'])
             output['symbol'].append(self.symbol)
             output['STO'].append(row['slowd'])
             output['price'].append(row['price'])
             output['adv'].append("SELL")
                # sell.append("Date: {0},price: {1} sell ,stochastic \r\n".format(row['date'],row['price']))
            elif row['slowk'] <= pSTO['buy'] and row['slowd'] <= pSTO['buy']:
                 output['date'].append(row['date'])
                 output['symbol'].append(self.symbol)
                 output['STO'].append(row['slowd'])
                 output['price'].append(row['price'])
                 output['adv'].append("BUY")
                # buy.append("Date: {0},price: {1} buy ,stochastic \r\n".format(row['date'],row['price']))
        return (pd.DataFrame(output).iloc[::-1])
        # return (pd.DataFrame(output))

    # Does MACD buy and sell analysis and returns a pandas dataframe
    def analyzeMACD(self,pMACD={'price':'close','fp':12,'sp':26,'slp':9}):
        df = self.df
        macd, macdsignal, macdhist = MACD(df[pMACD['price'].capitalize()], fastperiod=pMACD['fp'], slowperiod=pMACD['sp'], signalperiod=pMACD['slp'])
        data = {
            'date' : df['Date'],
            'macd' : round(macd,2),
            'macdsignal' : round(macdsignal,2),
            'macdhist' :round(macdhist,2),
            'price' : df['Close']
        }
        dff = pd.DataFrame(data)
        # dff.dropna(inplace=True) ##it is not working as sometimes i+1 is not avaliable
        output = {'date' : [],'symbol':[],'ind' : 'MACD','MACD' : [],'price' : [],'adv' : []}
        for i,v in dff.iterrows():
            if (i+1) < len(dff):
                #1. bullish signal as macd and signal line goes negative to positive,this is a buy signal.
                if dff.at[i,'macd'] > 0 and dff.at[i,'macdsignal'] > 0 and dff.at[(i-1),'macdsignal'] < 0:
                    # print(i,dff.at[i,'macd'],dff.at[i,'macdsignal'],dff.at[i,'date'])
                    # pass
                    output['date'].append(dff.at[i,'date'])
                    output['symbol'].append(self.symbol)
                    output['MACD'].append(dff.at[i,'macdsignal'])
                    output['price'].append(dff.at[i,'price'])
                    output['adv'].append("BUY")

                #2. buy signal if macd line crosses the signal line from below
                elif dff.at[i,'macd'] < dff.at[i,'macdsignal'] and dff.at[(i+1),'macd'] > dff.at[(i+1),'macdsignal']:
                    # print(i,dff.at[i,'macd'],dff.at[i,'macdsignal'],dff.at[i,'date'])
                    # print((i+1),dff.at[(i+1),'macd'],dff.at[(i+1),'macdsignal'],dff.at[(i+1),'date'])
                    # pass
                    output['date'].append(dff.at[(i+1),'date'])
                    output['symbol'].append(self.symbol)
                    output['MACD'].append(dff.at[(i+1),'macdsignal'])
                    output['price'].append(dff.at[(i+1),'price'])
                    output['adv'].append("BUY")
                
                #3. bearish signal as macd and signal line goes positive to negative,this is a sell signal.
                elif dff.at[i,'macd'] < 0 and dff.at[i,'macdsignal'] > 0 and dff.at[(i+1),'macdsignal'] < 0:
                    # print(i,dff.at[i,'macd'],dff.at[i,'macdsignal'],dff.at[i,'date'])
                    # pass
                    output['date'].append(dff.at[(i+1),'date'])
                    output['symbol'].append(self.symbol)
                    output['MACD'].append(dff.at[(i+1),'macdsignal'])
                    output['price'].append(dff.at[(i+1),'price'])
                    output['adv'].append("SELL")

                #4. sell signal if macd line crosses the signal line from above
                elif dff.at[i,'macd'] > dff.at[i,'macdsignal'] and dff.at[(i+1),'macd'] < dff.at[(i+1),'macdsignal']:
                    # print(i,dff.at[i,'macd'],dff.at[i,'macdsignal'],dff.at[i,'date'])
                    # print((i+1),dff.at[(i+1),'macd'],dff.at[(i+1),'macdsignal'],dff.at[(i+1),'date'])
                    output['date'].append(dff.at[(i+1),'date'])
                    output['symbol'].append(self.symbol)
                    output['MACD'].append(dff.at[(i+1),'macdsignal'])
                    output['price'].append(dff.at[(i+1),'price'])
                    output['adv'].append("SELL")
        return(pd.DataFrame(output).iloc[::-1])
        # return(pd.DataFrame(output))
                


class VisualizationTools():
    def __init__(self,dataframe):
        self.df = dataframe

    #This function plots the candlestick chart of a stock
    def plotStock(self,plot='candle'):
        df =  self.df
        if plot == 'Mountain':
            # pmin = MIN(df['Close'],timeperiod=50)
            pmin = [min(df['Close']) for i in range(len(df))]
            fa = go.Scatter(x=df['Date'],y=df['Close'],fill='tonexty',name=(df['Symbol'])[0],line_color='indigo')
            fb = go.Scatter(x=df['Date'],y=pmin,fill=None,line_color='indigo',name=' ')
            return (fb,fa)
        elif plot == 'candle':
            fc = go.Candlestick(x=df['Date'],
                            open=df['Open'],
                            high=df['High'],
                            low=df['Low'],
                            close=df['Close'],
                            increasing_line_color = 'cyan',
                            increasing_fillcolor = 'cyan',
                            decreasing_line_color = 'gray',
                            decreasing_fillcolor = 'gray',
                            name=(df['Symbol'])[0])
            return fc

    # This function plots trade volume along with candlestick chart of the stock
    def plotVolume(self):
        df = self.df
        pmin = min(df['Low'])
        pmax = max(df['High'])
        vmax = max(df['Volume'])
        pavg = (pmin+pmax)/2
        y = ((df['Volume']/vmax)*(pavg/5))
        bar = go.Bar(x=df['Date'],y=y, marker_color='rgba(26, 118, 255,0.4)',name='vol')
        return bar
    
    # This function plots MACD chart along with candlestick chart of the stock
    def plotMACD(self,pMACD={'price':'close','fp':12,'sp':26,'slp':9}):
        df = self.df
        dff = StockAnalysisTools(df).analyzeMACD()

        macd, macdsignal, macdhist = MACD(df[pMACD['price'].capitalize()], fastperiod=pMACD['fp'], slowperiod=pMACD['sp'], signalperiod=pMACD['slp'])
        # macd, macdsignal, macdhist = MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
        # macd.dropna(inplace=True)
        # macdsignal.dropna(inplace=True)
        fa = go.Scatter(x=df['Date'],y=macd,name='Macd',line_color='white')
        fb = go.Scatter(x=df['Date'],y=macdsignal,name='Signal',line_color='red')
        fc = go.Scatter(x=dff['date'],y=dff['price'],mode='markers',marker={'size':10,'color':'orange'},name='macd(B/S)')
        return fa,fb,fc

    # This function plots RSI chart
    def plotRSI(self,pRSI = {'time' : 14,'buy' : 70,'sell' : 30,'price' : 'Close'}):
        df = self.df
        dff = StockAnalysisTools(df).analyzeRSI()
        real = RSI(df[pRSI['price'].capitalize()], timeperiod=pRSI['time'])
        fo = go.Scatter(x=df['Date'],y=real,name='RSI',line_color='blue')
        fp = go.Scatter(x=dff['date'],y=dff['price'],mode='markers',marker={'size':7,'color':'green'},name='rsi(B/S)')
        return fo,fp

    # This function plots SMA or EMA chart along with candlestick chart of the stock
    def plotMA(self,pMA={'time':20,'price':'open','type':'SMA','name':'SMA'}):
        df = self.df
        if pMA['type'] == 'SMA':
            output = SMA(df[pMA['price'].capitalize()], timeperiod=pMA['time'])
        elif pMA['type'] == 'EMA':
            output = EMA(df[pMA['price'].capitalize()], timeperiod=pMA['time'])
        fo = go.Scatter(x=df['Date'],y=output,name=pMA['name'])
        return fo

    # This function plots Stochastics indicator along with candlestick chart of the stock
    def plotStochastics(self,pSTO={'buy':20,'sell':80,'fastkp':5, 'slowkp':3, 'slowkm':0, 'slowdp':3, 'slowdm':0}):
        df = self.df
        dff = StockAnalysisTools(df).analyzeStochastics()
        slowk, slowd = STOCH(df['High'], df['Low'], df['Close'], fastk_period=pSTO['fastkp'], slowk_period=pSTO['slowkp'], slowk_matype=pSTO['slowkm'], slowd_period=pSTO['slowdp'], slowd_matype=pSTO['slowdm'])
        # slowk, slowd = STOCH(df['High'], df['Low'], df['Close'], fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
        fa = go.Scatter(x=df['Date'],y=slowk,name='slowk',line_color='skyblue')
        fb = go.Scatter(x=df['Date'],y=slowd,name='slowd',line_color='yellow')
        fc = go.Scatter(x=dff['date'],y=dff['price'],mode='markers',marker={'size':7,'color':'pink'},name='sto(B/S)')

        return fa,fb,fc

    # This function plots Bollinger Bands
    def plotBB(self,pBB={'time':5,'price':'close','nbdevup':2,'nvdevdn':2,'matype':0}):
        df = self.df
        upperband, middleband, lowerband = BBANDS(df[pBB['price'].capitalize()], timeperiod=pBB['time'], nbdevup=pBB['nbdevup'], nbdevdn=pBB['nvdevdn'], matype=pBB['matype'])
        ub = go.Scatter(x=df['Date'],y=upperband,name='line')
        mb = go.Scatter(x=df['Date'],y=middleband,name='line')
        lb = go.Scatter(x=df['Date'],y=lowerband,name='line')
        return ub,mb,lb

    def findChartPattern():
        pass