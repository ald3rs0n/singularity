from Backend.tools import VisualizationTools as vt
from plotly import graph_objects as go
from app import *
import pandas as pd
from dash import Output,Input
from dash.exceptions import PreventUpdate



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


@app.callback(
    Output("output","figure"),
    [Input("storing", "data"),
    Input("switches-input", "value"),
    Input("toggle-switch", "value")],
)
def output_graph(data,indicator,tsh):

    # content = offcanvascontent(df,value2)
    if data is None or indicator is None:
        raise PreventUpdate
    # df = getData(stock)
    df = pd.read_json(data, orient='split')
    if df is None:
        raise PreventUpdate
    fig = makeGraph(df,indicator,tsh)
    if fig is None:
        raise PreventUpdate
    return fig