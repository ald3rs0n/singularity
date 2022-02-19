from logging import critical
from time import monotonic
import dash_bootstrap_components as dbc
from dash import Input, Output,State, html
from datetime import timedelta
import pandas as pd
from dash.exceptions import PreventUpdate
from webob import html_escape

from app import app
from Backend.dbconnect import getDataFromDB, getStockname
from Backend.connector import getData
from Backend.analysis import *
from Backend.settings import *
from Backend.tools import Utils,StockAnalysisTools as SAT

def generateHTMLTable(df):
    rows = []
    table_header = [
        html.Thead(html.Tr([html.Th("Date"), html.Th("Price"), html.Th("Suggestion"), html.Th("Indicator")]))
        ]
    symbol,dt = df.iloc[-1:-2:-1].get(["symbol",'date']).values[0]
    modalHeader = getStockname(symbol)
    for i,v in df.iterrows():
        for j in range(30) : 
            if v['date'] == str(TODAY - timedelta(days=j)):
                row = html.Tr([html.Td(v['date']), html.Td(v['price']), html.Td(v['adv']), html.Td(v['ind'])])
                rows.append(row)
        
    table_body = [html.Tbody(rows)]
    table = dbc.Table(table_header + table_body, bordered=True)
    table = dbc.Table(
        table_header + table_body,
        bordered=False,
        dark=False,
        hover=True,
        responsive=True,
        striped=True,
        )
    return table,modalHeader


def trendColor(trend):
    if trend == "Uptrend":
        return("green")
    elif trend == "Downtrend":
        return("red")



def generateOverviewTab(stock):
    utils = Utils()
    dt_week = datetime.date(datetime.now()) - WEEK
    dt_month = datetime.date(datetime.now()) - MONTH
    dt_half = datetime.date(datetime.now()) - HALFYEAR
    dt_year = datetime.date(datetime.now()) - YEAR

    query_week = {"Date" : {"$gt" : str(dt_week)}}
    query_month = {"Date" : {"$gt" : str(dt_month)}}
    query_half = {"Date" : {"$gt" : str(dt_half)}}
    query_year = {"Date" : {"$gt" : str(dt_year)}}


    df = getDataFromDB(stock)
    df_week  = getDataFromDB(stock,query_week)
    df_month  = getDataFromDB(stock,query_month)
    df_half  = getDataFromDB(stock,query_half)
    df_year  = getDataFromDB(stock,query_year)

    dayChange,_ = utils.dailyPercentageChangeCalc(df_week)
    weekly = utils.calcTimelyReturn(df_week)
    monthly = utils.calcTimelyReturn(df_month)
    halfyearly = utils.calcTimelyReturn(df_half)
    yearly = utils.calcTimelyReturn(df_year)

    sat = SAT(df_year)
    macd = sat.analyzeMACD()
    rsi = sat.analyzeRSI()
    sto = sat.analyzeStochastics()
    macd_year = analyzeIndicator(macd[::-1])
    rsi_year = analyzeIndicator(rsi[::-1])
    stoch_year = analyzeIndicator(sto[::-1])


    trend = trendAnalysis(df_week,2)
    color1 = trendColor(trend)
    trend7 = trendAnalysis(df_month,7)
    color7 = trendColor(trend7)
    trend30 = trendAnalysis(df_half,30)
    color30 = trendColor(trend30)
    
    cross = SAT(df).analyzeCross()
    if not cross.empty:
        cross = cross.at[0,'adv']+" on "+cross.at[0,'date']
    else:
        cross = ""

    overview = dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.H6("Trand"),
                        html.P("Today "+trend,style={'color':color1}),
                        html.P("Weekly "+trend7,style={'color':color7}),
                        html.P("Monthly "+trend30,style={'color':color30}),
                        html.P(cross)
                    ]),
                    dbc.Col([
                        html.H6("Return"),
                        html.P("Day "+str(dayChange)+" %"),
                        html.P("Weekly "+weekly),
                        html.P("Monthly "+monthly),
                        html.P("6 Months "+halfyearly),
                        html.P("Anually "+yearly),
                    ])
                ]),
                dbc.Row([
                    dbc.Col(html.P("MACD(1Y) "+macd_year)),
                    dbc.Col(html.P("RSI(1Y) "+rsi_year)),
                    dbc.Col(html.P("STO(1Y) "+stoch_year)),
                ])
            ])
    return overview



def makeModal(bodyContent,headerContent,overview):
    # table,tablename = generateHTMLTable(dfs)
    modal = html.Div(children=[
            dbc.Button("Analysis", id="open-lg", className="me-1", color="light",n_clicks=0),
                dbc.Modal(
                    [dbc.ModalHeader(dbc.ModalTitle(headerContent,id='table-modal-header')),
                    dbc.Tabs([
                        dbc.Tab(
                            [dbc.ModalBody(overview,id="overview-modal-body")],
                            label="Overview",
                            label_style={"background-color": "#222","padding":"0.5rem"},
                            active_label_style={"background-color": "#111"}
                            ),
                        dbc.Tab(
                            [dbc.ModalBody(bodyContent,id="table-modal-body")],
                            label="Indicator",
                            label_style={"background-color": "#222","padding":"0.5rem"},
                            active_label_style={"background-color": "#111"}
                            ),
                        dbc.Tab(
                            [dbc.ModalBody("candles coming soon",id="Candle-modal-body")],
                            label="Candle",
                            label_style={"background-color": "#222","padding":"0.5rem"},
                            active_label_style={"background-color": "#111"}
                            ),
                        dbc.Tab(
                            [dbc.ModalBody("patterns coming soon",id="pattern-modal-body")],
                            label="Patterns",
                            label_style={"background-color": "#222","padding":"0.5rem"},
                            active_label_style={"background-color": "#111"}
                            ),
                        ],
                        style={"flex-direction":'row'}
                    )],
                    id="modal-lg",
                    # style={"background-color":"rgba(22,22,22,0.5)"},
                    size="lg",
                    is_open=False,
                )]
            )
    return modal



def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open
app.callback(
    Output("modal-lg", "is_open"),
    Input("open-lg", "n_clicks"),
    State("modal-lg", "is_open"),
)(toggle_modal)


@app.callback([
    Output('table-modal-header', 'children'),
    Output('table-modal-body', 'children'),
    Output("overview-modal-body",'children'),  
    ],
    [Input("home_searchbar", "value"),
    Input("switches-input", "value"),
    ],
    # prevent_initial_call=True
)
def analysis_output(stock,indicator):
    if stock is None or indicator is None:
        raise PreventUpdate
    df = getData(stock)
    if df is None:
        raise PreventUpdate
    # dfs = doAnalysis(df,indicator)
    dfs = doAnalysis(df,['MACD','RSI','STOCH'])
    if dfs.empty:
        raise PreventUpdate
    table,modalHeader = generateHTMLTable(dfs)
    overview = generateOverviewTab(stock)
    return modalHeader,table,overview



