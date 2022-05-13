from dash import html,dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State

from app import app
from layoutComponents.dashbdwlModal import *
from layoutComponents.dashbdPortfolio import portfolio
from layoutComponents.dashbdSettingsRow import dashbdSettings
from layoutComponents.dashbdAnalysisRow import dashbdAnalysis




def dashbdNavLayout():   
    
    analysisrow = html.Div(
        [
            dbc.Button(html.Div(
                # "<??>",
                html.Img(src='static/analysis.ico'),
                id="open-analysis-canvas",
                n_clicks=0,
            ),color='light'),
            dbc.Offcanvas(html.Div(dashbdAnalysis()),
                id="analysis-canvas",
                scrollable=True,
                title="Buy ~ Sell",
                is_open=False,
                placement="end",
                # style={'textAlign' : 'center'}
            ),
        ]
    )
    home = dbc.Button(html.Div(
                dcc.Link('Home', href='/',style={'color':'#dddddd','text-decoration':'none'}),
            ),color='light')
    
    navbar = dbc.Navbar(
        dbc.Container(
            [
                dbc.Col(dbc.NavItem(dashbdSettings()),width={"size": 1, "order": "first"}),
                dbc.Col(dbc.NavItem(home)),
                # dbc.Col(dbc.NavItem()), 
                dbc.Col(dbc.NavbarToggler(id="navbar-toggler", n_clicks=0)),
                # dbc.Col(dbc.NavItem()),
                dbc.Col(dbc.NavItem(makeSearchBar('dashbd_searchbar'))),
                dbc.Col(dbc.NavItem(analysisrow),width={"size": 1,"offset": 1}),
                dbc.Col(dbc.NavItem(dbc.Button(html.Img(src='static/sync.ico'),id="sync",n_clicks=0,color='dark')),width={"size": 1, "order": "last"}),
            ],
        fluid=True,
        ),
        color="dark",
        dark=True,
        class_name="navbar navbar-light sticky-top",
    )
    return navbar


def dashbdBodyLayout():


    dashboardBody = dbc.Container([
        dbc.Row([
            dbc.Col(
                html.Div(makeWatchlist('dashbd_watchlist'),id='watchlist-container'),
                width={'size':3,'order':"last",'offset':9}
            )
        ]),
        dbc.Row(portfolio())
    ],fluid=True)
    return dashboardBody





@app.callback(
    Output('watchlist','children'),
    Input('dashbd_watchlist','value')
)
def watchliststock(value):
    if not value:
        raise PreventUpdate
    list_group = makeListForWatchlist(value)
    return list_group


# add callback for toggling the collapse on small screens

@app.callback(
    Output("tools-canvas", "is_open"),
    Input("open-tools-canvas", "n_clicks"),
    State("tools-canvas", "is_open"),
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open

@app.callback(
    Output("analysis-canvas", "is_open"),
    Input("open-analysis-canvas", "n_clicks"),
    State("analysis-canvas", "is_open"),
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open


@app.callback([
    Output('watchlist-container','children'),
    # Output('del-watchlist-container','children')
    ],
    Input('sync','n_clicks'),
    prevent_initial_call = True
)
def dosomething(n1):
    if n1:
        a =  makeWatchlist('dashbd_watchlist')
        # b =  makeWatchlist('del_watchlist')
        return [a]