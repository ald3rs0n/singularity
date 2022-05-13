from dash import html
from datetime import datetime
import  dash_bootstrap_components as dbc
from dash.dependencies import Input,Output,State

from app import app
from layoutComponents.makeComponents import *
from Backend.connector import getUpcomingDividend





def generateDividendTable():
    df = getUpcomingDividend()
    rows = []
    table_header = [
        html.Thead(
            html.Tr([
                html.Th("Symbol"), 
                html.Th("Type"), 
                html.Th("RS"), 
                # html.Th("Yield %"), 
                # html.Th("Announcement Date"),
                html.Th("Ex-Dividend Date"),
                html.Th("Record Date"),
                ]))
        ]
    # symbol,dt = df.iloc[-1:-2:-1].get(["symbol",'date']).values[0]
    # modalHeader = getStockname(symbol)
    modalHeader = "Upcoming Dividends"
    for i,v in df.iterrows():
        # for j in range(30) : 
            # if v['date'] == str(TODAY - timedelta(days=j)):
        symbol = v['symbol']
        # stock = Stock(symbol)
        ex_date = datetime.strftime(v['ex date'],"%d-%m-%Y")
        amount = float(v['%'])/10
        # div_yield = divYield(amount,stock.close)
        row = html.Tr([
                html.Td(symbol), 
                html.Td(v['type']), 
                html.Td(amount), 
                # html.Td(div_yield), 
                # html.Td(v['ann date']),
                html.Td(ex_date),
                html.Td(v['record date']),
                ])
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





def makeDividendModal():
    bodyContent,headerContent = generateDividendTable()
    modal = html.Div(children=[
            dbc.Button("Dividend", id="dividend-table", className="me-1", color="light",n_clicks=0),
                dbc.Modal(
                    [dbc.ModalHeader(dbc.ModalTitle(headerContent,id='dividend-table-modal-header')),
                    dbc.Tabs([
                        dbc.Tab(
                            [dbc.ModalBody(bodyContent,id="dividend-table-modal-body")],
                            label="Upcoming",
                            label_style={"background-color": "#222","padding":"0.5rem"},
                            active_label_style={"background-color": "#111"}
                            ),
                        ],
                        style={"flex-direction":'row'}
                    )],
                    id="dividend-modal-lg",
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
    Output("dividend-modal-lg", "is_open"),
    Input("dividend-table", "n_clicks"),
    State("dividend-modal-lg", "is_open"),
)(toggle_modal)


