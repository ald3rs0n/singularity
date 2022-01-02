import dash
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import html,dcc
import dash_daq as daq
from datetime import datetime,date,timedelta
import plotly.graph_objects as go
from backend.dbconnect import getDataFromDB
from backend.tools import VisualizationTools as vt
from backend.settings import STDF
from backend.connector import getData
from backend.analysis import doAnalysis
from app import app
from static.watchlist import W,getWatchlist

def makestocklist(stdf):
    options = []
    for i,v in stdf.iterrows():
        option = {"label" : v['NAME OF COMPANY'],"value" : v['SYMBOL']}
        options.append(option)
    return options

def makeOptions(watchlists):
    options = []
    for watchlist in watchlists:
        option = {"label" : watchlist,"value" : watchlist}
        options.append(option)
    return options

def makeGraph(df,args,tsh):  
        # df = getFileData(value)
        title = "Charts of {0}".format((df['Symbol'])[1])
        # title = "Charts of NULL"
        fig = go.Figure()
        r,c = 2,3
        fig.set_subplots(rows=r,cols=c,
                specs=[
                    [{'colspan' : 3},None,None],
                    [{},{},{}]
                    ],
                subplot_titles=(title,"","",""),
                vertical_spacing= 0.09,
                row_heights=[0.7,0.3],
                )
        # df = pd.read_csv('static/SBIN.csv')
        fig.update_layout(height=800,width=1350,
                        template="plotly_dark",
                        xaxis_rangeslider_visible=False,
                        showlegend=True)
        #
        if tsh:
            fig.add_trace(vt(df).plotStock())
        else:
            fig.add_traces(vt(df).plotStock(plot='Mountain'))
        set_row,set_col = 2,0
        for arg in args:
            x = arg.upper()
            # if x == 'MOUNTAIN':
            if x == 'MACD':
                set_col += 1
                fmacd,fsignal,buysell = vt(df).plotMACD()
                fig.add_traces((fmacd,fsignal), rows=[set_row,set_row], cols=[set_col,set_col])   
                fig.add_trace(buysell)
                fig.update_xaxes(title_text=x,row=set_row,col=set_col)
            elif x == 'RSI':
                set_col += 1
                rsignal,buysell = vt(df).plotRSI()
                fig.add_trace(rsignal,row=set_row,col=set_col)
                fig.update_xaxes(title_text=x,row=set_row,col=set_col)
                fig.add_trace(buysell)
            elif x == 'STOCH':
                set_col += 1
                stoch,stsignal,buysell = vt(df).plotStochastics()
                fig.add_traces((stoch,stsignal), rows=[set_row,set_row], cols=[set_col,set_col])
                fig.update_xaxes(title_text=x,row=set_row,col=set_col)
                fig.add_trace(buysell)
            elif x == 'BB':
                fig.add_traces(vt(df).plotBB())
                fig.update_xaxes(title_text='Bollinger Bands',row=1,col=1)
            elif x == 'SMA':
                fig.add_trace(vt(df).plotMA())
                fig.update_xaxes(title_text='SMA',row=1,col=1)
            elif x == 'EMA':
                fig.add_trace(vt(df).plotMA({'time':20,'price':'open','type':'EMA','name':'EMA'}))
                fig.update_xaxes(title_text='EMA',row=1,col=1)
            elif x == "VOL":
                bar = vt(df).plotVolume()
                base = min(df['Low'])
                fig.add_trace(bar)
                fig.update_traces(base=base,selector=dict(type='bar'))
                fig.update_xaxes(row=1,col=1)
        return fig
        # graph2 = dcc.Graph(figure=fig2)

def makeCards(watchlist,args):
        # dataframe = getFileData(value)
        options = makeOptions(W)
        select = dbc.Select(
            id="select",
            style={"color":"dark"},
            options=options,
            placeholder="Choose a watchlist"
            )
        cards = [select]
        wlist = getWatchlist(watchlist)
        for stockname in wlist:
            df = getDataFromDB(stockname)
            vals = doAnalysis(df,args)
            tdate = datetime.date(datetime.now())
            for val in vals:
                for i,v in val.iterrows():
                    # x = "Date : {0}\tPrice : {1} || {2}\r\n".format(v['date'],v['price'],(val.columns.values)[2])
                     for j in range(7) : 
                        if v['date'] == str(datetime.date(datetime.now()) - timedelta(days=j)):
                        # if v['date'] == str(tdate):
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
    
def offcanvascontent(stockname,args):
    
    cards = makeCards(stockname,args)       
    return html.Div(cards,id="output2"),

def navLayout(content):
    stocklist = makestocklist(STDF.iloc[::-1])
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
    
    search_bar = html.Div(dcc.Dropdown(id="pqrst",
                        options=stocklist,
                        className="dark",
                        placeholder="search a stock",
                        value="sbin"),style={'color':'#111111','background-color':'blue'})
        
    toolsrow = html.Div(
        [
            dbc.Button(
                "Tools",
                id="open-offcanvas-scrollable",
                n_clicks=0,
                color='light'
            ),
            dbc.Offcanvas(
                # html.P("List of tools goes here"),
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
            dbc.Offcanvas(content,
                # html.Div(children=[content]),
                id="offcanvas-scrollable2",
                scrollable=True,
                title="Buy ~ Sell",
                is_open=False,
                placement="end",
                # style={'textAlign' : 'center'}
            ),
        ]
    )
    navbar = dbc.Navbar(
        dbc.Container(
        # dbc.Row(
            [
                dbc.Col(dbc.NavItem(toolsrow)),
                # dbc.Col(dbc.NavItem(dbc.Input(id="input2",type="text",value='macd', placeholder="indicator", debounce=True))),
                dbc.Col(dbc.NavbarToggler(id="navbar-toggler", n_clicks=0)),
                # dbc.Col(dbc.NavItem()),
                # dbc.Col(dbc.NavItem()),
                # dbc.Col(dbc.NavItem()),
                dbc.Col(dbc.NavItem(search_bar)),
                dbc.Col(dbc.NavItem(analysisrow),width={"size": 1, "order": "last", "offset": 1}),
                # dcc.Store(id='stored-in-browser')
            ]
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
    Output('output', 'figure'),
    # Output('stored-in-browser','data')
    [Input("pqrst", "value"),
    Input("switches-input", "value"),
    Input("toggle-switch", "value")],
    # State("input", "valid"),
    prevent_initial_call=True
)
def output_graph(stock,indicator,tsh):

    # content = offcanvascontent(df,value2)
    if stock is None or indicator is None:
        raise PreventUpdate
    df = getData(stock)
    if df is None:
        raise PreventUpdate
    fig = makeGraph(df,indicator,tsh)
    if fig is None:
        raise PreventUpdate
    return fig

        


@app.callback(
    Output("output2","children"),
    Input("select","value"),
    Input("switches-input", "value"),
    prevent_initial_call=True
)
def select_output(sel,sw):
    # pass
    if sel is None or sw is None:
        raise PreventUpdate
    content = offcanvascontent(sel,sw)
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



