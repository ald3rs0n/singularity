import dash_bootstrap_components as dbc
from dash import Input, Output,State, html
from datetime import timedelta
from dash.exceptions import PreventUpdate

from app import app
from Backend.dbconnect import getDataFromDB
from Backend.analysis import doAnalysis
from Backend.settings import TODAY

def generateHTMLTable(dfs):
    rows = []
    table_header = [
        html.Thead(html.Tr([html.Th("Date"), html.Th("Price"), html.Th("Suggestion"), html.Th("Indicator")]))
        ]
    for df in dfs:
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
    return table
     
def makeModal(bodyContent):
    # table,tablename = generateHTMLTable(dfs)
    modal = html.Div(children=[
            dbc.Button("Analysis", id="open-lg", className="me-1", color="light",n_clicks=0),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("")),
                    dbc.ModalBody(bodyContent),
                ],
                id="modal-lg",
                size="lg",
                is_open=False,
            )])
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


@app.callback(
    Output('modal-lg', 'children'),
    [Input("home_searchbar", "value"),
    # Input("storing", "data"),
    Input("switches-input", "value"),
    # Input("open-lg", "n_clicks"),
    ],
    # prevent_initial_call=True
)
def analysis_output(stock,indicator):
    if stock is None or indicator is None:
        raise PreventUpdate
    df = getDataFromDB(stock)
    # df = pd.read_json(data, orient='split')
    if df is None:
        raise PreventUpdate
    dfs = doAnalysis(df,indicator)
    # print(dfs)
    table = generateHTMLTable(dfs)
    return table