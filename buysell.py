import pandas as pd
from Backend import *



def buyStock(name,quantity,price,date,target,indicator,stoploss):
    collection_db = singularitydb['transactions']
    quary = {
        'stock':name,
        'date':date,
        'buy_price':price,
        'quantity':quantity,
        'target':target,
        'indicator':indicator,
        'stoploss':stoploss
        }
    pass



