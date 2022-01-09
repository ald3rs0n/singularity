from talib import *
from Backend.settings import P_RSI,P_MACD,P_STO
from Backend.tools import StockAnalysisTools as SAT

# Does analysis on a single dataframe on given indicators and retunrs list of dataframe of buy and sell options
def doAnalysis(df,args):
    output = []
    sat = SAT(df)
    for arg in args:
        if arg.upper() == "RSI":
            rsi = sat.analyzeRSI(P_RSI)
            output.append(rsi.iloc[0:5])
        elif arg.upper() == "STOCH":
            sto = sat.analyzeStochastics(P_STO)
            output.append(sto.iloc[0:5])
        elif arg.upper() == "MACD":
            macd = sat.analyzeMACD(P_MACD)
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
