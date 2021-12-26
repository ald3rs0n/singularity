import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import html,dcc
import plotly.graph_objects as go
from plotly.subplots import make_subplots as ms
from backend.tools import VisualizationTools as vt
from backend.getdata import getFileData
from backend.analysis import doAnalysis
from app import app

def makeGraph(df,args):
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
        fig.add_trace(vt(df).plotStock())
        set_row,set_col = 2,0
        for arg in args:
            x = arg.upper()
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
                fig.add_trace(vt(df).plotMA({'time':20,'price':'open','type':'EMA'}))
                fig.update_xaxes(title_text='EMA',row=1,col=1)
        return fig
        # graph2 = dcc.Graph(figure=fig2)

def canvas2Data(dataframe,value2):
        # dataframe = getFileData(value)
        cards = []
        vals = doAnalysis(dataframe,value2)
        for val in vals:
            for i,v in val.iterrows():
                # x = "Date : {0}\tPrice : {1} || {2}\r\n".format(v['date'],v['price'],(val.columns.values)[2])
                x = "Date : {0}\tPrice : {1} || {2}\r\n".format(v['date'],v['price'],v['ind'])
                if v['adv'] == "SELL":
                    style = {'color' : 'cyan'}
                elif v['adv'] == "BUY":
                    style = {'color' : 'orange'}
                title = v['adv']+' : '+v['symbol']
                card = dbc.Card([
                    # dbc.CardImg(),
                    dbc.CardBody([
                        html.H5(title,className="card-title"),
                        html.P(x,className="card-text"),
                        # html.P(v['symbol'],className="card-text"),
                        # dbc.Button()
                    ])
                ],style=style)
                cards.append(card)
        return cards
    
def offcanvascontent(value,value2):
    cards = canvas2Data(value,value2)
    return html.Div(cards,id="output2"),

def navLayout(content):

    switches = html.Div(
        [
            dbc.Label("Toggle a Indicator"),
            dbc.Checklist(
                options=[
                    {"label": "MACD", "value": 'macd'},
                    {"label": "RSI", "value": 'rsi'},
                    # {"label": "STOCH", "value": 'stoch', "disabled": True},
                    {"label": "STOCH", "value": 'stoch'},
                    {"label": "Bollinger Band", "value": 'bb',"disabled": True},
                    {"label": "SMA", "value": 'sma'},
                    {"label": "EMA", "value": 'ema'},
                ],
                value=['macd'],
                inline=True,
                id="switches-input",
                switch=True,
            ),
        ]
    )
    search_bar = dbc.Row(
        [
            dbc.Col(dbc.Input(id="input",type="text",value="sbin", placeholder="Search", debounce=True)),
            # dbc.Col(
            #     dbc.Button(
            #         "Search", color="primary", className="ms-2", n_clicks=0
            #     ),
            #     width="auto",
            # ),
            # dbc.Col(html.P(id="output"))
        ],
        className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
        align="center",
    )
    offcanvas = html.Div(
        [
            dbc.Button(
                "Tools",
                id="open-offcanvas-scrollable",
                n_clicks=0,
            ),
            dbc.Offcanvas(
                # html.P("List of tools goes here"),
                html.Div(switches),
                id="offcanvas-scrollable",
                scrollable=True,
                title="Scrollable Offcanvas",
                is_open=False,
                placement="start"
            ),
        ]
    )  
    offcanvas2 = html.Div(
        [
            dbc.Button(
                "<??>",
                id="open-offcanvas-scrollable2",
                n_clicks=0,
            ),
            dbc.Offcanvas(content,
                # html.Div(children=cards),
                # graph,
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
                dbc.Col(dbc.NavItem(offcanvas)),
                # dbc.Col(dbc.NavItem(dbc.Input(id="input2",type="text",value='macd', placeholder="indicator", debounce=True))),
                dbc.Col(dbc.NavbarToggler(id="navbar-toggler", n_clicks=0)),
                # dbc.Col(dbc.NavItem()),
                # dbc.Col(dbc.NavItem()),
                # dbc.Col(dbc.NavItem()),
                # dbc.Col(dbc.NavItem()),
                dbc.Col(dbc.Collapse(
                    search_bar,
                    id="navbar-collapse",
                    is_open=False,
                    navbar=True,
                )),
                dbc.Col(
                    dbc.NavItem(offcanvas2),
                    width={"size": 1, "order": "last", "offset": 1},),
                # dcc.Store(id='stored-in-browser')
            ]
        ),
        color="dark",
        dark=True,
        class_name="navbar sticky-top",
    )
    return navbar



# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

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
    [Output('output', 'figure'),
    Output('output2','children')],
    # Output('stored-in-browser','data')
    [Input("input", "value"),
    Input("switches-input", "value")],
    # prevent_initial_call=True
)
def output_text(value,value2):
    df = getFileData(value)
    # fig = makeGraph(value,value2)
    # content = offcanvascontent(value,value2)
    fig = makeGraph(df,value2)
    content = offcanvascontent(df,value2)
    return fig,content
    # return df
    
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



