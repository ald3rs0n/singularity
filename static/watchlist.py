import pandas as pd
from datetime import date
# list on names on watchlists
W = ['BANKS','TELECOM','TECHNOLOGY','ENERGY','STARTUPS','FMCG','FINTECH','IPOS','MEDICAL','AUTOMOBILE']

# Lists of stocks accrding to their sectors
BANKS = ['sbin','rblbank','yesbank','icicibank','idbi','hdfcbank','axisbank','iob','kotakbank','indusindbk','bandhanbnk']
TECHNOLOGY = ['infy','nazara','tataelxsi','hcltech','techm','wipro','mindtree','tcs','zentec'] #????
ENERGY = ['ongc','kiocl','iex','tatapower','adanipower','powergrid']
STARTUPS =['nykaa','zomato']
TELECOM = ['idea','bhartiartl']
FINTECH = ['paytm','bajajfinsv']
IPOS =['zomato','datapattns','latentview']
MEDICAL = ['sunpharma','drreddy','cipla','divislab','cadilahc','sigachi']
FMCG = ['itc','marico','hindunilvr']
AUTOMOBILE = ['tatamotors','eichermot','heromotoco','tvsmotor']

#Stocks accoridng to their capitals
LARGECAP = ['reliance'] #>5000Cr
MIDCAP = [] #1000-5000Cr
SMALLCAP = [] #<1000Cr

#High dividend paying stocks
HIGHDIV = ['ongc','nmdc',]

wlist = {'BANKS' : BANKS,
        'TELECOM' : TELECOM,
        'TECHNOLOGY' : TECHNOLOGY,
        'ENERGY' : ENERGY,
        'STARTUPS' : STARTUPS,
        'FMCG' : FMCG,
        'FINTECH' : FINTECH,
        'IPOS' : IPOS,
        'MEDICAL' : MEDICAL,
        'AUTOMOBILE' : AUTOMOBILE}


def updateWatchlist(watchlist,stock):
    wlist = watchlist.upper()
    wlist.append(stock)
    return wlist

def getWatchlist(wl):
    return wlist.get(wl)

# print(getWatchlist('TELECOM'))


st = pd.read_csv("static/stocks.csv")

