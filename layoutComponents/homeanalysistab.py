# from nsetools import Nse
from datetime import timedelta
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash import Input, Output,State, html

from app import app
from Backend.analysis import *
from Backend.settings import *
# from Backend.connector import getData
from Backend.stock import Stock
from Backend.dbconnect import getDataFromDB
from Backend.tools import Utils,StockAnalysisTools as SAT




def trendColor(trend):
    if trend == "Uptrend":
        return("green")
    elif trend == "Downtrend":
        return("red")


def generateTabs(stock):
    this = Stock(stock)
# def generateHTMLTable(this):
    # modalHeader = getStockname(symbol)
    modalHeader = this.name
    dfs = this.df
    if dfs is None:
        raise PreventUpdate
    df = doAnalysis(dfs,['MACD','RSI','STOCH'])
    if df.empty:
        raise PreventUpdate
    rows = []
    table_header = [
        html.Thead(html.Tr([html.Th("Date"), html.Th("Price"), html.Th("Suggestion"), html.Th("Indicator")]))
        ]
    # symbol,dt = df.iloc[-1:-2:-1].get(["symbol",'date']).values[0]
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
    # return table,modalHeader



# def generateOverviewTab(this):
    stock = this.symbol
    utils = Utils()
    dt_week = datetime.date(datetime.now()) - WEEK
    dt_month = datetime.date(datetime.now()) - MONTH
    dt_half = datetime.date(datetime.now()) - HALFYEAR
    dt_year = datetime.date(datetime.now()) - YEAR

    query_week = {"Date" : {"$gt" : str(dt_week)}}
    query_month = {"Date" : {"$gt" : str(dt_month)}}
    query_half = {"Date" : {"$gt" : str(dt_half)}}
    query_year = {"Date" : {"$gt" : str(dt_year)}}


    # df = getDataFromDB(stock)
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
    macd = sat.analyzeMACD(P_MACD)
    rsi = sat.analyzeRSI(P_RSI)
    sto = sat.analyzeStochastics(P_STO)
    macd_year = analyzeIndicator(macd[::-1])
    rsi_year = analyzeIndicator(rsi[::-1])
    stoch_year = analyzeIndicator(sto[::-1])


    trend = trendAnalysis(df_week,2)
    color1 = trendColor(trend)
    trend7 = trendAnalysis(df_month,7)
    color7 = trendColor(trend7)
    trend30 = trendAnalysis(df_half,30)
    color30 = trendColor(trend30)
    
    cross = SAT(this.df).analyzeCross()
    if not cross.empty:
        cross = cross['adv'].iloc[0:1] +" on "+cross['date'].iloc[0:1]
        # print(cross)
    else:
        cross = ""


    std = flactuation(this.df)


    overview = dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.H6("Trand"),
                        html.P("Today "+trend,style={'color':color1}),
                        html.P("Weekly "+trend7,style={'color':color7}),
                        html.P("Monthly "+trend30,style={'color':color30}),
                        html.P(cross),
                        html.P(f"STD:  {std}")
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
    # return overview



# def generateInfoTab(this):
    fundamentals = this.fundamentals()
    info = dbc.Container([
            dbc.Row([
                dbc.Col([
                    # dbc.Row(this.purpose),
                    dbc.Row(f"Dividend: {this.dividend()}"),
                    dbc.Row(f"Div Yield: {this.divYield()} %"),
                    dbc.Row(f"Ex Date: {this.ex_date}"),
                    dbc.Row(f"Record Date: {this.record_date}"),
                    ]),
                dbc.Col([
                    dbc.Row(f"52 week High: {this.high52}"),
                    dbc.Row(f"52 week Low: {this.low52}"),
                    dbc.Row(f"Book Value: {fundamentals['Book Value/Share']}"),
                    dbc.Row(f"Face Value: {fundamentals['Face value']}"),
                    ]),
                dbc.Col([
                    dbc.Row(f"EPS: {fundamentals['EPS ']}"),
                    dbc.Row(f"PE Ratio: {fundamentals['Price / EPS (PE)']}"),
                    dbc.Row(f"PB Ratio: {fundamentals['Price / Book ']}"),
                    dbc.Row(f"ROE: {fundamentals['ROE']}"),
                    dbc.Row(f"D2E: {fundamentals['Debt To Equity']}"),
                    ]),
            ]),
    ])

    details = dbc.Container([
            dbc.Row([
                dbc.Col([f"{fundamentals['Details']}"]),
                ])
    ])
    return modalHeader,table,overview,info,details

def makeModal(bodyContent,headerContent,overview,info,details):
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
                        dbc.Tab(
                            [dbc.ModalBody(info,id="info-modal-body")],
                            label="Info",
                            label_style={"background-color": "#222","padding":"0.5rem"},
                            active_label_style={"background-color": "#111"}
                            ),
                        dbc.Tab(
                            [dbc.ModalBody(details,id="details-modal-body")],
                            label="Details",
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
    Output("info-modal-body",'children'),  
    Output("details-modal-body",'children'),  
    ],
    [Input("home_searchbar", "value"),
    Input("switches-input", "value"),
    ],
    # prevent_initial_call=True
)
def analysis_output(stock,indicator):
    if stock is None or indicator is None:
        raise PreventUpdate
    # df = getData(stock)
    # nse = Nse()
    # stk = nse.get_quote(stock)
    # this = Stock(stock)
    # df = this.df
    # if df is None:
    #     raise PreventUpdate
    # dfs = doAnalysis(df,indicator)
    # dfs = doAnalysis(df,['MACD','RSI','STOCH'])
    # if dfs.empty:
    #     raise PreventUpdate
    # table,modalHeader = generateHTMLTable(this)
    # overview = generateOverviewTab(this)
    # info,details = generateInfoTab(this)
    
    modalHeader,table,overview,info,details = generateTabs(stock)
    return modalHeader,table,overview,info,details



