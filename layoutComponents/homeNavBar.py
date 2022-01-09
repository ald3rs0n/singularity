from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import html,dcc
import dash_daq as daq
from datetime import timedelta

from app import app
from Backend.dbconnect import getDataFromDB,getWatchlist
from Backend.connector import getData
from Backend.settings import TODAY,WEEK,WATCHLISTPERIOD,BOOL
from Backend.analysis import doAnalysis
from layoutComponents.makeComponents import *


def makeCards(watchlist,args,on):
    if watchlist and args:
        wlist,_id = getWatchlist(watchlist)      
        cards = []
        for stockname in wlist:
            if on:
                df = getData(stockname,WEEK)
            else:
                df = getDataFromDB(stockname)
            vals = doAnalysis(df,args)
            for val in vals:
                for i,v in val.iterrows():
                     for j in range(WATCHLISTPERIOD) : 
                        if v['date'] == str(TODAY - timedelta(days=j)):
                            x = "Date : {0}\tPrice : {1} || {2}\r\n".format(v['date'],v['price'],v['ind'])
                            if v['adv'] == "SELL":
                                style = {'color' : 'cyan'}
                            elif v['adv'] == "BUY":
                                style = {'color' : 'orange'}
                            title = v['adv']+' : '+v['symbol']
                            card = dbc.Card([
                                dbc.CardBody([
                                    html.H5(title,className="card-title"),
                                    html.P(x,className="card-text"),
                                ])
                            ],style=style)
                            cards.append(card)
        return cards
    
def offcanvascontent(stockname,args,on=True):
    
    cards = makeCards(stockname,args,on)       
    return html.Div(cards,id="output2"),

def navLayout(content,modal):

    switches = html.Div(
        [
            dbc.Label("Indicators"),
            html.Br(),
            daq.ToggleSwitch(
                id='toggle-switch',
                value=True,
                color="cyan",
                label="Candlestick",
                labelPosition='top',
            ),
            html.Br(),
            dbc.Checklist(
                options=[
                    # {"label": "STOCK", "value": 'Mountain'},
                    {"label": "MACD", "value": 'macd'},
                    {"label": "RSI", "value": 'rsi'},
                    # {"label": "STOCH", "value": 'stoch', "disabled": True},
                    {"label": "STOCH", "value": 'stoch'},
                    {"label": "Bollinger Band", "value": 'bb',"disabled": True},
                    {"label": "SMA", "value": 'sma'},
                    {"label": "EMA", "value": 'ema'},
                    {"label": "Volume", "value": 'VOL'},
                ],
                value=['macd'],
                inline=True,
                id="switches-input",
                switch=True,
            ),
        ]
        )
    
        
    toolsrow = html.Div(
        [
            dbc.Button(
                "Tools",
                id="open-offcanvas-scrollable",
                n_clicks=0,
                color='light'
            ),
            dbc.Offcanvas(
                html.Div(switches),
                id="offcanvas-scrollable",
                scrollable=True,
                title="Indicators Settings",
                is_open=False,
                placement="start"
            ),
        ]
    )  
    analysisrow = html.Div(
        [
            dbc.Button(html.Div(
                # "<??>",
                html.Img(src='static/analysis.ico'),
                id="open-offcanvas-scrollable2",
                n_clicks=0,
            ),color='light'),
            dbc.Offcanvas(html.Div([
                html.Div(makeWatchlist('home_watchlist'),id='wlist-container'),
                html.Div(content)]),
                id="offcanvas-scrollable2",
                scrollable=True,
                title="Buy ~ Sell",
                is_open=False,
                placement="end",
                # style={'textAlign' : 'center'}
            ),
        ]
    )
    dashboard = dbc.Button(html.Div(
                dcc.Link('Dashboard', href='/dashboard',style={'color':'#dddddd','text-decoration':'none'}),
            ),color='light')
    
    navbar = dbc.Navbar(
        dbc.Container(
            [
                dbc.Col(dbc.NavItem(toolsrow)),
                dbc.Col(dbc.NavItem(dashboard)),
                dbc.Col(dbc.NavItem(modal)),
                dbc.Col(dbc.NavbarToggler(id="navbar-toggler", n_clicks=0)),
                # dbc.Col(dbc.NavItem()),
                dbc.Col(dbc.NavItem(makeSearchBar('home_searchbar'))),
                dbc.Col(dbc.NavItem(analysisrow),width={"size": 1, "offset": 1}),
                dbc.Col(dbc.NavItem(dbc.Button(html.Img(src='static/sync.ico'),id="sync",n_clicks=0,color='dark')),width={"size": 1, "order": "last"}),
            ],
            fluid=True,
        ),
        color="dark",
        dark=True,
        class_name="navbar navbar-light sticky-top",
    )
    return navbar



# add callback for toggling the collapse on small screens
@app.callback(
    Output("offcanvas-scrollable", "is_open"),
    Input("open-offcanvas-scrollable", "n_clicks"),
    State("offcanvas-scrollable", "is_open"),
)
def toggle_offcanvas_scrollable(n1, is_open):
    if n1:
        return not is_open
    return is_open

@app.callback(
    Output("offcanvas-scrollable2", "is_open"),
    Input("open-offcanvas-scrollable2", "n_clicks"),
    State("offcanvas-scrollable2", "is_open"),
)
def toggle_offcanvas_scrollable2(n1, is_open):
    if n1:
        return not is_open
    return is_open



@app.callback(
    Output("output2","children"),
    Input("home_watchlist","value"),
    Input("switches-input", "value"),
    prevent_initial_call=True
)
def select_output(sel,sw):
    # pass
    if sel is None or sw is None:
        raise PreventUpdate
    content = offcanvascontent(sel,sw,on=BOOL)
    return content




@app.callback(
    Output('toggle-switch', 'label'),
    Input('toggle-switch', 'value')
)
def update_output(value):
    if value:
        return 'Candlestick'
    else:
        return 'Mountain'

# @app.callback(
    #     [Output('output','figure'),
    #     Output('output2','children')],
    #     Input('stored-in-browser','data'),
    #     prevent_initial_call = True
    # )
    # def output_text(data):
    #     fig = makeGraph(data)
    #     content = offcanvascontent(data)
    #     return fig,content
@app.callback(
    Output('wlist-container','children'),
    Input('sync','n_clicks'),
    prevent_initial_call = True
)
def dosomething(n1):
    if n1:
        return makeWatchlist('home_watchlist')


