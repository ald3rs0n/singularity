from dash import html,Output,Input
import dash_bootstrap_components as dbc
from time import sleep


from app import app
from Backend.dbconnect import updateStockList
from layoutComponents.dashbdwlModal import makeWatchlistModal


def dashbdSettings():
    settings = html.Div(
            [
                dbc.Button(
                    # "Settings",
                    html.Img(src='static/cog.ico'),                
                    id="open-tools-canvas",
                    n_clicks=0,
                    color='light'
                ),
                dbc.Offcanvas(
                    html.Div([
                        dbc.Row([
                            dbc.Col(makeWatchlistModal(" ")),
                        ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col(
                                dbc.Button(
                                    dbc.Spinner(html.Div(id="updating"),size='sm'),
                                    id='update-stocklist',
                                    color='light',className="me-1"),
                                className="d-grid gap-2"
                                ), 
                        ])
                    ]),
                    id="tools-canvas",
                    scrollable=True,
                    title="Settings",
                    is_open=False,
                    placement="start"
                ),
            ]
        )
    return settings



@app.callback(
    Output('updating','children'),
    Input('update-stocklist','n_clicks'),
    prevent_initial_callback = True
)
def update(n1):
    if n1:
        # sleep(2)
        updateStockList()
        return "Update stocklist"
    return "Update stocklist"