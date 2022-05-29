import dash
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output,State
from dash import html

from app import app
from Backend.dbconnect import *
from layoutComponents.makeComponents import *



def input_group_create_watchlist():
    input_group_create_watchlist = dbc.InputGroup(dbc.Row(
        [
            dbc.Col(dbc.Input(id="input-group-text-input", placeholder="name of watchlist",debounce=True)),
            dbc.Col(makeSearchBar('cwl_searchbar'),width={'size':4}),
            dbc.Col(dbc.Button("ADD", id="input-group-button",color="light", n_clicks=0),width={'size':2}),
        ]
    ),style={'display':'block'})
    return input_group_create_watchlist


@app.callback(
    [Output("cwl_searchbar", "value"),
    Output("input-group-text-input", "value"),
    Output("input-group-button", "n_clicks")],
    [Input("cwl_searchbar", "value"),
    Input("input-group-text-input", "value"),
    Input("input-group-button", "n_clicks")],
    prevent_initial_callback = True
)
def on_button_click(stock,w_name,n_clicks):
    if n_clicks:
        if stock is None or w_name is None or not w_name or not stock:
            raise PreventUpdate
        ret = createWatchlist(w_name,stock)
        print(ret)
        return None,None,0
    else:
        raise PreventUpdate


def input_group_delete_watchlist():
    input_group_delete_watchlist = dbc.InputGroup(dbc.Row(
        [
            dbc.Col(html.Div(makeWatchlist('del_watchlist'),id="del-watchlist-container"),width={'size':4}),
            dbc.Col(dbc.Button("DEL", id="delete-group-button",color="light", n_clicks=0),width={'size':2}),
        ]
    ),style={'display':'block'})
    return input_group_delete_watchlist


@app.callback(
    [Output("del_watchlist", "value"),
    Output("delete-group-button", "n_clicks")],
    # Output("black_whole", "value"),
    [Input("del_watchlist", "value"),
    Input("delete-group-button", "n_clicks")],
    prevent_initial_callback = True
)
def on_button_click(w_name,n_clicks):
    if n_clicks:
        if w_name is None or not w_name:
            raise PreventUpdate
        deleteWatchlist(w_name)
        print("Watchlist Deleted")
        return '',0
    else:
        raise PreventUpdate


def input_group_modify_watchlist():
    input_group_modify_watchlist = dbc.InputGroup([
        dbc.Row([
                # dbc.Col(dbc.Input(id="input-group-text-input", placeholder="name of watchlist",debounce=True)),
                # dbc.Col(makeWatchlist('mod_watchlist'),width={'size':4}),
                dbc.Col(dbc.Button("Add Stock", id="add-modify-group-button",color="light", n_clicks=0),width={'size':4}),
                dbc.Col(dbc.Button("Remove Stock", id="remove-modify-group-button",color="light", n_clicks=0),width={'size':4}),
            ]),
        dbc.Row([
            dbc.Col(html.Div(id="modify")),
            ])],
        style={'display':'block'})
    return input_group_modify_watchlist



def input_group_add_m_watchlist():
    input_group_add_m_watchlist = dbc.InputGroup([
        dbc.Row([dbc.Col(html.Br())]),
        dbc.Row(
        [
            dbc.Col(makeWatchlist('add_modify_watchlist'),width={'size':4}),
            dbc.Col(makeSearchBar('mwl_searchbar')),
            dbc.Col(dbc.Button("ADD", id="add-m-button",color="light", n_clicks=0),width={'size':2}),
        ]
    )],style={'display':'block'})
    return input_group_add_m_watchlist


@app.callback(
    [Output("mwl_searchbar", "value"),
    Output("add-m-button", "n_clicks")],
    [Input("add_modify_watchlist", "value"),
    Input("mwl_searchbar", "value"),
    Input("add-m-button", "n_clicks")],
    prevent_initial_callback = True
)
def on_button_click(w_name,stock,n_clicks):
    print(w_name,stock)
    if n_clicks:
        if stock is None or w_name is None or not w_name or not stock:
            raise PreventUpdate
        # ret = "Adding "+stock+" to "+w_name
        ret = addStockToWatchlist(w_name,stock)
        print(ret)
        return None,0
    else:
        raise PreventUpdate



def input_group_remove_m_watchlist():
    input_group_remove_m_watchlist = dbc.InputGroup([
        dbc.Row([dbc.Col(html.Br())]),
        dbc.Row(
        [   
            dbc.Col(makeWatchlist('remove_modify_watchlist')),
            dbc.Col(html.Div(id="remove_stock_list")),
            dbc.Col(dbc.Button("REMOVE", id="remove-m-button",color="light", n_clicks=0),width={'size':2}),
        ]
    )],style={'display':'block'})
    return input_group_remove_m_watchlist

@app.callback(
    Output('remove_stock_list','children'),
    Input('remove_modify_watchlist','value')
)
def renderstocklist(value):
    return(makeStocklist('remove_modify_stock_list',value))



@app.callback(
    [Output('remove_modify_stock_list','value'),
    Output('remove-m-button','n_clicks')],
    [Input('remove_modify_watchlist','value'),
    Input('remove_modify_stock_list','value'),
    Input("remove-m-button",'n_clicks')],
    prevent_initial_call = True
)
def removestockfromlist(w_list,stock,n1):
    print(w_list,stock,n1)
    if n1:
        if w_list is None or not w_list or stock is None or  not stock:
            raise PreventUpdate
        ret = deleteStockFromWatchlist(w_list,stock)
        print(ret)
        return '',0
    else:
        raise PreventUpdate









@app.callback(
    Output('modify','children'),
    Input('add-modify-group-button','n_clicks'),
    Input('remove-modify-group-button','n_clicks'),
    prevent_initial_call = True
)
def addstocktowatchlist(n1,n2):
    if n1%2:
        return input_group_add_m_watchlist()
    elif n2%2:
        return input_group_remove_m_watchlist()
    else:
        return None

def makeWatchlistModal(bodyContent):
    modal = html.Div(children=[
            dbc.Button("Edit Watchlists", id="open-w-modal", className="me-1", color="light",n_clicks=0),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Hola Juan!")),
                    dbc.Row([
                        dbc.Col(
                            dbc.Button("Create Watchlist", id="create-w", className="me-1", color="light",n_clicks=0),
                        ),
                        dbc.Col(
                            dbc.Button("Delete Watchlist", id="delete-w", className="me-1", color="light",n_clicks=0),
                        ),
                        dbc.Col(
                            dbc.Button("Modify Watchlist", id="modify-w", className="me-1", color="light",n_clicks=0),
                        ),
                    # dbc.Button("Watchlist", id="create-w", className="me-1", color="light",n_clicks=0),
                    ]),
                    dbc.ModalBody(html.Div(bodyContent,id="create")),
                ],
                id="modal-w",
                size="lg",
                is_open=False,
            )],className="d-grid gap-2")
    return modal

@app.callback([
    Output("create",'children'),
    Output('create-w',"n_clicks"),
    Output('delete-w',"n_clicks"),
    Output('modify-w',"n_clicks")],
    Input('create-w',"n_clicks"),
    Input('delete-w',"n_clicks"),
    Input('modify-w',"n_clicks"),
    prevent_initial_call = True
)
def create_w(cn1,dn1,mn1):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    if cn1%2:
        return input_group_create_watchlist(),cn1,0,0
    elif dn1%2:
        return input_group_delete_watchlist(),0,dn1,0
    elif mn1%2:
        return input_group_modify_watchlist(),0,0,mn1
        return
    else:
        return "",0,0,0
    


def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open

app.callback(
    Output("modal-w", "is_open"),
    Input("open-w-modal", "n_clicks"),
    State("modal-w", "is_open"),
)(toggle_modal)
