import dash_bootstrap_components as dbc
from dash import html,Input,Output
from dash.exceptions import PreventUpdate
from datetime import datetime

from app import app
from Backend.dbconnect import getNamesFromPortfolio, getPortfiloData, getStockname, updatePortfolioData
from layoutComponents.makeComponents import makeSearchBar



def buy_form():
    buy = dbc.InputGroup([
                makeSearchBar('buy_searchbar'), 
                html.Br(),
                dbc.Row([
                    dbc.Col(dbc.Input(id="buy_price", placeholder="price",type="number",debounce=True),style={'padding':0}),
                    dbc.Col(dbc.Input(id="quantity", placeholder="quantity",type="number",debounce=True),style={'padding':0}),
                ],class_name="mb-3"),
                dbc.Row([
                    dbc.Col(dbc.Input(id="stoploss", placeholder="stop loss",type="number",debounce=True),style={'padding':0}),
                    dbc.Col(dbc.Input(id="target", placeholder="target",type="number",debounce=True),style={'padding':0}),
                ],class_name="mb-3"),
                dbc.Row([
                    dbc.Col(dbc.Input(id="indicator",placeholder="indicator or pattern",debounce=True),style={'padding':0}),
                    dbc.Col(dbc.Input(id="buy_date",placeholder="YYYY-mm-dd",debounce=True),style={'padding':0}),
                ],class_name="mb-3"),
                dbc.Row([
                    dbc.Button("BUY", id="buy",color="light", n_clicks=0),
                ],class_name="mb-3")
            ],
            style={'display':'block'})
    return buy


@app.callback(
    [Output('buy','n_clicks'),
    Output('buy_searchbar','value'),
    Output('buy_price','value'),
    Output('quantity','value'),
    Output('stoploss','value'),
    Output('target','value'),
    Output('indicator','value'),
    Output('buy_date','value'),
    Output('return-text','children')],

    [Input('buy_searchbar','value'),
    Input('buy_price','value'),
    Input('quantity','value'),
    Input('stoploss','value'),
    Input('target','value'),
    Input('indicator','value'),
    Input('buy_date','value'),
    Input('buy','n_clicks')]
)
def buy_stock(stock,price,quantity,stoploss,target,indicator,buy_date,n0):
    regex = datetime.strptime
    if (stock is None) or (price is None) or (price == 0) or (quantity is None) or (quantity == 0) or (buy_date is None) or (target is None) or (target == 0) or (stoploss is None) or (stoploss == 0) or (indicator is None):
        raise PreventUpdate
    else:
        if n0%2:
            try:
                buy_date = str(datetime.date(regex(buy_date,"%Y-%m-%d")))
                updatePortfolioData("BUY",stock,buy_date,price,quantity,target,indicator,stoploss)
                print(stock,price,quantity,buy_date,stoploss,target,indicator,n0)
                print("Updating slowly...")
                return 0,None,None,None,None,None,None,None,"Updated"
            except ValueError:
                raise PreventUpdate
        else:
            raise PreventUpdate


def makeSellList():
    stocks = getNamesFromPortfolio()
    options = []
    for stock in stocks:
        name = getStockname(stock)
        option = {"label" : name, "value" : stock}
        options.append(option)
    selectStock = dbc.Select(
        id="sell_searchbar",
        style={"color":"dark"},
        options=options,
        placeholder="Choose a stock",
        )
    return selectStock
 
def sell_form():
    sell = dbc.InputGroup([
                html.Br(),
                dbc.Row([makeSellList()],class_name="mb-3"), 
                dbc.Row([
                    dbc.Col(dbc.Input(id="sell_price", placeholder="price",type="number",debounce=True),style={'padding':0}),
                    dbc.Col(dbc.Input(id="sell_quantity", placeholder="quantity",type="number",debounce=True),style={'padding':0}),
                ],class_name="mb-3"),
                dbc.Row([
                    dbc.Input(id="sell_date",placeholder="YYYY-mm-dd",debounce=True)
                ],class_name="mb-3"),
                dbc.Row([
                    dbc.Button("SELL", id="sell",color="light", n_clicks=0),
                ],class_name="mb-1")
            ],
            style={'display':'block'})
    return sell

@app.callback(
    [Output('sell','n_clicks'),
    Output('sell_searchbar','value'),
    Output('sell_price','value'),
    Output('sell_quantity','value'),
    Output('sell_date','value'),
    Output('sell-return-text','children')],

    [Input('sell_searchbar','value'),
    Input('sell_price','value'),
    Input('sell_quantity','value'),
    Input('sell_date','value'),
    Input('sell','n_clicks')],
    prevent_initial_call = True
)
def sell_stock(stock,price,quantity,sell_date,n0):
    regex = datetime.strptime
    if (price is None) or (price == 0) or (quantity is None) or (quantity == 0) or (sell_date is None):
        if not stock is None:
            pf_dict = getPortfiloData(stock)
            # print(pf_dict)
            return 0,stock,pf_dict['buy_price'],pf_dict['quantity'],pf_dict['date'],""
        else:
            return 0,None,None,None,None,""
    else:
        if n0%2:
            try:
                sell_date = str(datetime.date(regex(sell_date,"%Y-%m-%d")))
                updatePortfolioData("SELL",stock,sell_date,price,quantity)
                # print(stock,price,quantity,sell_date,n0)
                # print("Updating slowly...")
                return 0,None,None,None,None,"Updated"
            except ValueError:
                raise PreventUpdate
        else:
            raise PreventUpdate


def dashbdAnalysis():
    container = dbc.Container([
        dbc.Row([
            dbc.Col(dbc.Button("BUY",id="buy-0",color='light',className="me-1",n_clicks=0),className="d-grid gap-2"),
            dbc.Col(dbc.Button("SELL",id="sell-0",color='light',className="me-1",n_clicks=0),className="d-grid gap-2"),
        ]),
        html.Br(),
        dbc.Row(id="op-form"),
        dbc.Row(html.P(id="return-text")),
        dbc.Row(html.P(id="sell-return-text")),
    ])
    return container

@app.callback(
    Output("op-form",'children'),
    Input("buy-0","n_clicks"),
    Input("sell-0","n_clicks"),
)
def makeForm(buy_n0,sell_n0):
    if buy_n0%2:
        return buy_form()
    elif sell_n0%2:
        return sell_form()
    else:
        return ""