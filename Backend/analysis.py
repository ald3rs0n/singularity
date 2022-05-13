from datetime import date, datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

from Backend.connector import getData
from Backend.dbconnect import getPortfiloData
from Backend.settings import P_RSI,P_MACD,P_STO
from Backend.tools import StockAnalysisTools as SAT, Utils

# Does analysis on a single dataframe on given indicators and retunrs list of dataframe of buy and sell options
def doAnalysis(df,args):
    rsi,macd,sto = pd.DataFrame(),pd.DataFrame(),pd.DataFrame()
    if not df is None:
        sat = SAT(df)
        for arg in args:
            if arg.upper() == "RSI":
                rsi = sat.analyzeRSI(P_RSI)
            elif arg.upper() == "STOCH":
                sto = sat.analyzeStochastics(P_STO)
            elif arg.upper() == "MACD":
                macd = sat.analyzeMACD(P_MACD)
            else:
                print("Invalid Operation : "+arg+"\r\n")
        rsi.drop_duplicates(inplace=True)
        rsi.reset_index(drop=True,inplace=True)
        macd.drop_duplicates(inplace=True)
        macd.reset_index(drop=True,inplace=True)
        sto.drop_duplicates(inplace=True)
        sto.reset_index(drop=True,inplace=True)
        new_df = pd.concat((rsi.iloc[0:5],macd.iloc[0:5],sto.iloc[0:5]),axis=0)
        if not new_df.empty :
            new_df.sort_values(by='date',inplace=True,ascending=False)
        return new_df


#Function for analyze stokcs in portfolio
def ananlyzePortfolio(stock):
    # x = getPortfiloData(stock)
    # df = getDataFromDB(stock)
    df = getData(stock)
    dt = Utils.dateCalc()
    sat = SAT(df)

    rsi = sat.analyzeRSI(P_RSI)
    sto = sat.analyzeStochastics(P_STO)
    macd = sat.analyzeMACD(P_MACD)
    new_df = pd.concat((rsi.iloc[0:5],macd.iloc[0:5],sto.iloc[0:5]))
    new_df.sort_values(by='date',inplace=True,ascending=False)
    
    new_df = new_df.iloc[0:5]
    suggestion,details = '',''
    for i,v in new_df.iterrows():
        vdt =datetime.date(datetime.strptime(v['date'],"%Y-%m-%d"))
        if vdt == dt or vdt == (dt- timedelta(days=1)):
            # if v['price'] > x['buy_price'] and v['adv'] == 'SELL':
            if v['adv'] == 'SELL':
                suggestion = v['adv']
                details = f"{v['ind']} hit on {v['date']} at {v['price']}"
                return suggestion,details
            else:
                suggestion = "HOLD"
                return suggestion,details
        else:
            suggestion = "HOLD"
            return suggestion,details



def analyzeIndicator(advdf):
    startmoney = 5000
    currentmoney = 5000
    endmoney = 5000
    currentstocks = 0
    buy  = 0 
    for i,v in advdf.iterrows():
        if v['adv'] == "BUY" and currentmoney > v['price']:
                recentstocks = int(currentmoney/v['price'])
                currentstocks += recentstocks
                currentmoney = int(currentmoney - (recentstocks*v['price']))
                endmoney = currentmoney + (currentstocks*v['price'])
                buy = v['price']
        elif v['adv'] == "SELL" and currentstocks > 0 and v['price'] > buy:
                if int(currentstocks*v['price']) > startmoney:
                    currentmoney += int(currentstocks*v['price'])
                    currentstocks = 0
                    endmoney = currentmoney
    if currentstocks == 0:
        ret = int(((endmoney-startmoney)/startmoney)*100)
        if ret > 0:
            return("Profit : "+str(ret)+" %")
        elif ret < 0:
            return("Loss : "+str(ret)+" %")
        elif ret == 0:
            return("No Trade")
    else:
        money = currentmoney + (currentstocks*buy)
        ret = int(((money-startmoney)/startmoney)*100)
        return("Expected :"+str(ret)+" %")


def trendAnalysis(df,time):
    """
        A function to analyze trand if it is uptrand or downtrand by calculating slope of the SMA curve.
        return : up trend.down trend,(?)no trend
    """
    # df.dropna(inplace=True).reset_index(drop=True,inplace=True)
    
    
    # scaler = MinMaxScaler(feature_range=(0,100))
    # reshaped_arr = df.values.reshape(-1,1)
    # scaled = scaler.fit_transform(reshaped_arr)
    # scaled_df = pd.Series(scaled.reshape(-1))
    # print(scaled_df.to_string())
    
    
    sat = SAT(df)
    slope_df = sat.analyzeSMA(pMA={'time':time,'price':'close','type':'SMA','name':'SMA'})
    
    scaled_df = pd.Series(slope_df)

    slope = (scaled_df[0:1]).to_list()[0]
    trand = ''
    if slope > 0:
        trand = "Uptrend"
    # elif 0.5 > slope > -0.5:
        # print(slope)
        # trand = "NO trend"
    elif slope < 0:
        trand = "Downtrend"
    return trand


def flactuation(df):
    scaler = MinMaxScaler(feature_range=(0,100))
    dff = df.iloc[-1:-22:-1]
    scaled_df = scaler.fit_transform(dff['Close'].values.reshape(-1,1))
    # scaled_df = scaler.fit_transform(df['Close'].values.reshape(-1,1))
    # v = scaled_df.var()
    s = scaled_df.std()
    return(str(round(s,2)))




# takes list of buy and sell dataframe and writes to a csv file
def writetocsv(vals):
    for val in vals:
        try:
            val.to_csv('analyzed/'+val.at[0,'symbol']+'_'+(val.columns.values)[2]+'.csv')
        except:
            pass
