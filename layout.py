import dash_bootstrap_components as dbc
from dash import html,dcc
from pandas.core.frame import DataFrame
import plotly.graph_objects as go
from plotly.subplots import make_subplots as ms
from tools import VisualizationTools as vt
from getdata import getFileData
from analysis import doAnalysis


def makeGraph(value):
        df = getFileData(value)
        title = "Charts of {0}".format((df['Symbol'])[1])
        fig = go.Figure()
        fig = ms(rows=2,cols=3,
                specs=[[{'colspan' : 3},None,None],[{},{},{}]],
                subplot_titles=(title,"MACD","RSI","Stochastics"),
                vertical_spacing= 0.09,
                row_heights=[0.7,0.3],
                )
        # df = pd.read_csv('static/SBIN.csv')
        fig.update_layout(height=800,width=1350,
                        template="plotly_dark",
                        xaxis_rangeslider_visible=False,
                        showlegend=False)
        fig.add_trace(vt(df).plotStock())
        # fig.add_traces(vt(df).plotBB())
        fig.add_trace(vt(df).plotSMA())
        fig.add_trace(vt(df).plotEMA())
        macd,macdsignal = vt(df).plotMACD()
        fig.add_traces([macd,macdsignal], rows=[2,2], cols=[1,1])
        fig.add_trace(vt(df).plotRSI(),row=2,col=2)
        a,b = vt(df).plotStochastics()
        fig.add_traces([a,b], rows=[2,2], cols=[3,3])
        return fig
        # graph2 = dcc.Graph(figure=fig2)

def canvas2Data(value):
        dataframe = getFileData(value)
        cards = []
        vals = doAnalysis(dataframe,'rsi','stoch')
        for val in vals:
            for i,v in val.iterrows():
                x = "Date : {0}\tPrice : {1} || {2}\r\n".format(v['date'],v['price'],(val.columns.values)[2])
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
    
def offcanvascontent(value):
    cards = canvas2Data(value)
    return html.Div(cards,id="output2"),

def makeLayout(content):

    search_bar = dbc.Row(
        [
            dbc.Col(dbc.Input(id="input",type="text", placeholder="Search", debounce=True)),
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
                html.P("List of tools goes here"),
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
                placement="end"
            ),
        ]
    )
    navbar = dbc.Navbar(
        dbc.Container(
            [
                dbc.NavItem(offcanvas),
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                dbc.Collapse(
                    search_bar,
                    id="navbar-collapse",
                    is_open=False,
                    navbar=True,
                ),
                dbc.NavItem(offcanvas2),
                dcc.Store(id='stored-in-browser')
            ]
        ),
        color="dark",
        dark=True,
    )
    return navbar
