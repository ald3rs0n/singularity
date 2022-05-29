from dash import html
import dash_daq as daq
from time import sleep
from math import exp,pow
import dash_bootstrap_components as dbc

# from app import app
from Backend.tools import Utils
from Backend.stock import Stock
from Backend.analysis import ananlyzePortfolio
from Backend.dbconnect import getNamesFromPortfolio,getPortfiloData
from Backend.ThreadWithResult import ThreadWithResult






def desmos_color_calc(ret_prcent):
    if ret_prcent > 0:
        green = hex(round(100 + 155*pow((1-exp(-0.06*ret_prcent)),4.5))).split('x')[-1]
        color = "#00"+str(green)+"00"
    elif ret_prcent < 0:
        red = hex(round(100+155*pow((1-exp(-0.06*abs(ret_prcent))),4.5))).split('x')[-1]
        color = "#"+str(red)+"0000"
    elif ret_prcent == 0:
        color = "#111111"
    return color


def make_pf_card(pf_stock):
    stock = Stock(pf_stock)
    utils = Utils()
        # stockname = stock.name
    df = stock.df
    # stockname = getStockname(stock)
    # df = getData(stock)
    pf_dict = getPortfiloData(pf_stock)

    dt,close = (df.iloc[-1:-2:-1].get(["Date","Close"]).values[0])

    updown,dtt = utils.dailyPercentageChangeCalc(df)
    buy_date,ret_amnt,ret_prcent,vol,init_price,invested,profit = utils.returnCalc(df,pf_dict)

    suggestion,details = ananlyzePortfolio(stock.symbol)

    daily_return = (updown*vol*close)/100
    


    if len(stock.name) > 20:
        cardtitle = stock.symbol
    else:
        cardtitle = stock.name.upper()

    bordercolor = desmos_color_calc(ret_prcent)
    # desmossize = desmos_size_calc(ret_amnt)
    desmossize = '10rem'
    height = desmossize
    width = height
    h6margin = '0.5rem'
    # if height > "12rem":
    #     h6margin = "1.5rem"

    target = pf_dict['target']
    stoploss = pf_dict['stoploss']
    # target = 10000
    # stoploss = 1
    if close >= target:
        bagde_text = 'T'
        bagde_color = 'success'
    elif close <= stoploss:
        bagde_text = 'S'
        bagde_color = 'danger'
    else:
        bagde_text = ''
        bagde_color = 'danger'


    card = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H6(cardtitle, className="card-title",style={'margin':h6margin,'font-size':'small'}),
                    html.P("Current : "+str(ret_amnt),style={"margin":"0px",'font-size':'smaller'}),
                    html.P("Advice : "+suggestion,style={"margin":"0px",'font-size':'smaller'}),
                    html.P("Return : "+str(ret_prcent)+" %",style={"margin":"0px",'font-size':'smaller'}),
                    dbc.Badge(
                        bagde_text,
                        color=bagde_color,
                        pill=True,
                        text_color="white",
                        className="position-absolute top-0 start-100 translate-middle",
                        )
                ],id=cardtitle,style={'text-align':'center'}
            ),
            dbc.Tooltip([
                    html.P(dtt,style={"margin":0}),
                    html.P("Invested : "+str(invested),style={"margin":0}),
                    html.P("Buying Price : "+str(init_price),style={"margin":0}),
                    # html.P("Buying Date : "+buy_date,style={"margin":0}),
                    html.P("Quantity : "+str(vol),style={"margin":0}),
                    html.P("Today : "+str(close)+"("+str(updown)+"%)",style={"margin":0}),
                    html.P("T "+str(target)+" || S "+str(stoploss),style={"margin":0}),
                    html.P(details)
                ],target=cardtitle,placement="top-start"
            ),
        ],
        style={"width":width,'height':height,'border-radius':"50%",'border':'10px solid','border-color':bordercolor,'background-color':"#010101"},
        )
    col_cards = dbc.Col(card,width={'size':3},style={'margin-bottom':'1rem'})
    return col_cards,profit,daily_return


def portfolio():
    pf_stocks = getNamesFromPortfolio()
    pf_cols = []
    cards = []
    daily_total_return = []
    profit_list = []
    
    threads = []
    for pf_stock in pf_stocks:
        # col_cards,profit,daily_return = make_pf_card(pf_stock)

        newThread = ThreadWithResult(target=make_pf_card,args=(pf_stock,))
        newThread.start()
        threads.append(newThread)
    
    for thread in threads:
        thread.join()
        try:
            col_cards,profit,daily_return = thread.result
            # print(b)
        except Exception as e:
            # print(e)
            pass

        daily_total_return.append(daily_return)
        profit_list.append(profit)
        cards.append(col_cards)

    col0 = dbc.Col(
                html.Div(id='empty'),
                width={'size':1,'order':"first"})
    pf_cols.append(col0)
    col1 = dbc.Col(
            html.Div(dbc.Container([
                dbc.Row([
                    dbc.Col(
                        daq.Gauge(
                            color={"gradient":True,"ranges":{"red":[-10000,4000],"yellow":[4000,5000],"green":[5000,10000]}},
                            scale={'start': -10000, 'interval': 2500, 'labelInterval': 2},
                            showCurrentValue=True,
                            id="profit-loss",
                            label='Total Return',
                            max=10000,
                            # size=175,
                            units="INR",
                            min=-10000,
                            style={'color':"#00ff00"},
                            value=sum(profit_list),
                        )
                    ),
                    dbc.Col(
                        daq.Gauge(
                            color={"gradient":True,"ranges":{"red":[-2000,900],"yellow":[900,1000],"green":[1000,2000]}},
                            scale={'start': -2000, 'interval': 250, 'labelInterval': 2},
                            showCurrentValue=True,
                            id="daily-profit-loss",
                            label='Daily Return',
                            max=2000,
                            min=-2000,
                            size=175,
                            units="INR",
                            style={'color':"#00ff00"},
                            value=round(sum(daily_total_return),2),
                        )
                    ),
                ],justify='center',align='center'),
                dbc.Row(cards,justify='center',align='center')
                ]),
                id='dashbd-portfolio'),
                width={'size':8},
        )
    pf_cols.append(col1)
    col2 = dbc.Col(
                dbc.Spinner(html.Div(id='watchlist'),size="md",type='grow'),
                width={'size':3,'order':"last"}
            )
    pf_cols.append(col2)
    return pf_cols