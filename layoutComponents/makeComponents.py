from dash.dash import Dash
from dash.html.Div import Div
import dash_bootstrap_components as dbc
from dash import html,dcc,Input,Output,State

from app import app
from Backend.dbconnect import getStocksList, getWatchlistNames,getWatchlist,getStocksList
from Backend.tools import Utilis
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
                        optionHeight=50),style={'color':'#111111','background-color':'blue'})
    return search_bar

def makeListForWatchlist(watchlist_name):
    """
    This function takes name of a watchlist and returns a html list of names of stocks in that list 
    """
    utilis = Utilis()
    watchlist,_id = getWatchlist(watchlist_name)
    item_list = []
    for stock in watchlist:
        getData(stock,BOOL,WEEK)
        dailyPriceChange,Date = utilis.dailyPercentageChangeCalc(stock)
        if dailyPriceChange >= 0 and dailyPriceChange < 2:
            color = "cyan"
        elif dailyPriceChange >= 2:
            color = "green"
        elif dailyPriceChange <0:
            color = "red"
        item = dbc.ListGroupItem(dbc.Row([
            dbc.Col([
                html.P(stock.upper(),className="mb-1"),
                ],
                # html.Small("OK!", className="text-success"),
            ),
            dbc.Col([
                html.P(str(dailyPriceChange)+" %",className="mb-1",style={'color':color}),
            ]),
            dbc.Col([
                html.Small(Date,className="mb-1"),
                # dbc.Button("Del",color="light"),
                ],
                width={'order':"last"},
            )
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
        style={"color":"dark"},
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
 
