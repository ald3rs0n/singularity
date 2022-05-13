from Backend.dbconnect import getStockname
from Backend.settings import P_BB, P_MA, P_MACD, P_RSI, P_STO, QUARTER, TODAY, YEAR
from Backend.tools import VisualizationTools as vt
from plotly import graph_objects as go
from app import *
import pandas as pd
from dash import Output,Input
from dash.exceptions import PreventUpdate
from Backend.connector import getData


def makeGraph(df,args,tsh):
        symbol = (df['Symbol'])[1]
        name = getStockname(symbol)

        y_range_min = min(df['Low'].tail(90))
        y_range_max = max(df['High'].tail(90))

        title = "Charts of {0}".format(name)
        fig = go.Figure(
            layout=go.Layout(
                # hovermode="x",
                # hoverdistance=100,
                # spikedistance=1000,
                # xaxis=dict(
                #     showspikes=True,
                #     spikecolor="#222",
                #     spikemode="across"
                #     )
                ))
        r,c = 2,3
        fig.set_subplots(rows=r,cols=c,
                specs=[
                    [{'colspan' : 3},None,None],
                    [{},{},{}]
                    ],
                subplot_titles=(title,"","",""),
                vertical_spacing= 0.09,
                row_heights=[0.7,0.3],
                # xaxis=dict(showspikes=True),
                )
        fig.update_layout(height=800,width=1350,
                        template="plotly_dark",
                        margin=dict(
                            b=10,
                            l=80,
                            t=40,
                            r=10,
                            pad=20
                        ),
                        dragmode="pan",
                        xaxis_showgrid=False,
                        # yaxis_showgrid=False,
                        xaxis=dict(
                            rangebreaks=[
                                dict(bounds=["sat", "mon"]), #hide weekends
                                # dict(values=["2015-12-25", "2016-01-01"])  # hide Christmas and New Year's
                            ],
                            range=[str(TODAY-QUARTER),str(TODAY)],
                            rangeselector=dict(
                                buttons=list([
                                    dict(count=1,
                                        label="1m",
                                        step="month",
                                        stepmode="backward"),
                                    dict(count=3,
                                        label="3m",
                                        step="month",
                                        stepmode="backward"),
                                    dict(count=6,
                                        label="6m",
                                        step="month",
                                        stepmode="backward"),
                                    dict(count=1,
                                        label="1y",
                                        step="year",
                                        stepmode="backward"),
                                    dict(step="all")
                                ]),
                                yanchor="top",
                                bgcolor="#222",
                            ),
                            rangeslider=dict(
                                # autorange=False,
                                visible=False
                            ),
                            type="date"
                        ),
                        yaxis=dict(
                            range=[y_range_min,y_range_max]
                        ),
                        showlegend=True)
        if tsh:
            fig.add_trace(vt(df).plotStock())
        else:
            fig.add_traces(vt(df).plotStock(plot='Mountain'))
        set_row,set_col = 2,0
        for arg in args:
            x = arg.upper()
            if x == 'MACD':
                set_col += 1
                fmacd,fsignal,buysell = vt(df).plotMACD(pMACD=P_MACD)
                fig.add_traces((fmacd,fsignal), rows=[set_row,set_row], cols=[set_col,set_col])   
                fig.add_trace(buysell)
                fig.update_xaxes(title_text=x,row=set_row,col=set_col)
            elif x == 'RSI':
                set_col += 1
                rsignal,buysell = vt(df).plotRSI(pRSI=P_RSI)
                fig.add_trace(rsignal,row=set_row,col=set_col)
                fig.update_xaxes(title_text=x,row=set_row,col=set_col)
                fig.add_trace(buysell)
            elif x == 'STOCH':
                set_col += 1
                stoch,stsignal,buysell = vt(df).plotStochastics(pSTO=P_STO)
                fig.add_traces((stoch,stsignal), rows=[set_row,set_row], cols=[set_col,set_col])
                fig.update_xaxes(title_text=x,row=set_row,col=set_col)
                fig.add_trace(buysell)
            elif x == 'BB':
                fig.add_traces(vt(df).plotBB(pBB=P_BB))
                fig.update_xaxes(title_text='Bollinger Bands',row=1,col=1)
            elif x == 'SMA':
                fig.add_trace(vt(df).plotMA(pMA=P_MA))
                fig.update_xaxes(title_text='SMA',row=1,col=1)
            elif x == 'EMA':
                fig.add_trace(vt(df).plotMA({'time':20,'price':'close','type':'EMA','name':'EMA'}))
                fig.update_xaxes(title_text='EMA',row=1,col=1)
            elif x == 'CROSS':
                fig.add_trace(vt(df).plotMA({'time':50,'price':'close','type':'SMA','name':'SMA-50'}))
                fig.add_trace(vt(df).plotMA({'time':200,'price':'close','type':'SMA','name':'SMA-200'}))
                fig.update_xaxes(title_text='SMA(50 & 200)',row=1,col=1)
            elif x == "VOL":
                bar = vt(df).plotVolume()
                base = min(df['Low'])
                fig.add_trace(bar)
                fig.update_traces(base=base,selector=dict(type='bar'))
                fig.update_xaxes(row=1,col=1)

        # fig.show(config={"displayModeBar": False, "showTips": False})
        return fig


@app.callback(
    Output("output","figure"),
    [
    Input("home_searchbar", "value"),
    Input("switches-input", "value"),
    Input("toggle-switch", "value")],
)
def output_graph(stock,indicator,tsh):
    if stock is None or indicator is None:
        raise PreventUpdate
    df = getData(stock)
    if df is None:
        raise PreventUpdate
    fig = makeGraph(df,indicator,tsh)
    if fig is None:
        raise PreventUpdate
    return fig





