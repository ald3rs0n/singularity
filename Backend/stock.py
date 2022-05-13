import re

from Backend.connector import getData,getQuote
from Backend.StockFundamentals import get_fundamentals



class Stock():
    def __init__(self,sym):
        stock = getQuote(sym)
        self.open = stock['open']
        self.date =  stock['date']
        self.low = stock['dayLow']
        self.low52 = stock['low52']
        self.high = stock['dayHigh']
        self.symbol = stock['symbol']
        self.high52 = stock['high52']
        self.ex_date = stock['exDate']
        self.purpose = stock['purpose']
        self.name = stock['companyName']
        self.close = stock['closePrice']
        self.face_value = stock['faceValue']
        self.record_date = stock['recordDate']
        self.previous_close = stock['previousClose']
        self.delivery_quantity = stock['deliveryQuantity']

        self.df = getData(self.symbol)

    def fundamentals(self):
        fundamental = get_fundamentals(self.symbol)
        return fundamental
    def dividend(self):
        ptn = '((RS |RE )[0-9.]+)'
        dividend = (str((re.findall(ptn,self.purpose))[0][0])[2::])
        return dividend


    def divYield(self):
        dividend = self.dividend()
        dY = 0
        try:
            dY = round((float(dividend)/float(self.close))*100,2)
            return dY   
        except ValueError:
            return dY
