from dash.dash import Dash
from dash.html.Div import Div
import dash_bootstrap_components as dbc
from dash import html,dcc,Input,Output,State

from app import app
from Backend.dbconnect import getStocksList, getWatchlistNames,getWatchlist,getStocksList
from Backend.tools import Utils
from Backend.settings import BOOL,WEEK
from Backend.connector import getData


def makeSearchBar(id):
    STDF = getStocksList()
    options = []
    for i,v in STDF.iterrows():
        option = {"label" : v['NAME OF COMPANY'],"value" : v['SYMBOL']}
        options.append(option)
    search_bar = html.Div(dcc.Dropdown(id=id,
                        options=options,
                        className="dark",
                        placeholder="search a stock",
                        # value="sbin",
                        optionHeight=50,
                        style={'background-color':'#222','color':'#111','border':'none','.Select-placeholder':{'color':'#fff'}}))
    return search_bar

def makeListForWatchlist(watchlist_name):
    """
    This function takes name of a watchlist and returns a html list of names of stocks in that list 
    """
    utilis = Utils()
    watchlist,_id = getWatchlist(watchlist_name)
    item_list = []
    for stock in watchlist:
        df = getData(stock,WEEK)
        if not df is None:
            price = (df.tail(1))['Close']
            dailyPriceChange,Date = utilis.dailyPercentageChangeCalc(df)
            if dailyPriceChange >= 0 and dailyPriceChange < 2:
                color = "cyan"
            elif dailyPriceChange >= 2:
                color = "#00ff00"
            elif dailyPriceChange <0:
                color = "red"
            item = dbc.ListGroupItem(
                    dbc.Row([
                        dbc.Col([html.P(stock.upper(),className="mb-1")]),
                        dbc.Col([html.P(str(dailyPriceChange)+" %",className="mb-1",style={'color':color})]),
                        dbc.Col([
                            html.P(price,className="mb-1"),
                            # html.Small(Date,className="mb-1")
                            ],
                            width={'order':"last"},
                            style={'color':color}),
                    ]),
                )
            item_list.append(item)
    return (dbc.ListGroup(item_list))


black_whole = html.Div(id="black_whole")

def makeWatchlist(id):
    watchlists = getWatchlistNames()
    options = []
    for watchlist in watchlists:
        option = {"label" : watchlist,"value" : watchlist}
        options.append(option)
    # return options
    # options = makeWatchlist()
    selectWatchlist = dbc.Select(
        id=id,
        style={"color":"white",'background-color':'#222'},
        options=options,
        placeholder="Choose a watchlist",
        )
    return selectWatchlist
 


def makeStocklist(id,watchlist):
    stocks,_id = getWatchlist(watchlist)
    options = []
    for stock in stocks:
        option = {"label" : stock.upper(), "value" : stock}
        options.append(option)
    # return options
    # options = makeWatchlist()
    selectStock = dbc.Select(
        id=id,
        style={"color":"dark"},
        options=options,
        placeholder="Choose a stock",
        )
    return selectStock
 
