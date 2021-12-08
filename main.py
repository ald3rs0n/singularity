from nsetools import Nse
from pprint import pprint
import re
from time import sleep
from datetime import datetime

ptn = '((RS |RE )[0-9.]+)'

nse = Nse()
#function that returns output to terminal
def terminalOutput(count,totalStocks,key,companyName,purpose,dividend,exDividendDate,dY,basePrice,upcoming):
    if dY > 2:
        print("|\t\033[0;36m {0:78}/{1} \033[0m|".format(count,totalStocks))
        print("|\t {0:10} : {1:70} |".format(key,companyName))
        print("|\t\033[32;1m {0:82} \033[0m |".format(purpose))
        print("|\t Dividend of RS {0:68} |".format(dividend))
        if upcoming:
            print("|\t\033[32;1m Ex Dividend Date : {0:64}\033[0m |".format(exDividendDate))
        else:
            print("|\t Ex Dividend Date : {0:64} |".format(exDividendDate))
        print("|\t Base Price : {0:70} |".format(basePrice))
        if dY >= 4 :
            print("|\t Dividend Yield : \033[32;1m{0:66}\033[0m |".format(dY))
        elif dY >= 2 and dY < 4 :
            print("|\t Dividend Yield : \033[1;33m{0:66}\033[0m |".format(dY))
        else:
            pass
            # print("|\t Dividend Yield : {0:66} |".format(dY))
        print("|"+92*'-'+"|")

#function that returns output to a file
def fileOutput(f,g,companyName,purpose,exDividendDate,dividendYield,dividend,basePrice,upcoming):
    if dividendYield >= 2:
        addToFileF = companyName+","+purpose+","+exDividendDate+","+str(dividendYield)+","+dividend+","+str(basePrice)+"\r\n"
        f.write(addToFileF)
    if upcoming:
        addToFileG = companyName+","+exDividendDate+","+str(dividendYield)+","+dividend+","+str(basePrice)+"\r\n"
        g.write(addToFileG)

# a class for different utilities
class Utilis():
    #function calculates dividend yield
    def divYield(div,basePr):
        dY = 0
        try:
            dY = round((float(div)/float(basePr))*100,2)
            return dY   
        except ValueError:
            return dY
    
    #function to find if there is upcoming dividend
    def findUpcomingDividend(exDividendDate):
        month = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
        exDD = ""
        for i in month:
            if exDividendDate[3:6] == i :
                exDD = exDividendDate.replace(exDividendDate[3:6],str(month.index(i)+1))

        date = datetime.now().strftime("%d-%m-%y")
        if int(exDD[6:8]) > int(date[6:8]):
            return True
        elif int(exDD[6:8]) == int(date[6:8]) and int(exDD[3:5]) > int(date[3:5]):
            return True
        elif int(exDD[6:8]) == int(date[6:8]) and int(exDD[3:5]) == int(date[3:5]) and int(exDD[0:2]) >= int(date[0:2]):
            return True
        else:
            return False

    #function to extract dividend amount from purpose column
    def dividendMatch(purpose,ptn):
        dividend = (str((re.findall(ptn,purpose))[0][0])[2::])
        return dividend

    #returns boolean if purpose is dividend or not
    def getPurpose(purpose):
        try:
            pp = str((re.findall("DIVIDEND",purpose))[0])
            if pp == "DIVIDEND":
                return True
            else:
                return False
        except IndexError:
            return False
        except TypeError:
            return False

def dividend(nse,ptn):
    # Create files to write output
    fname = "NSE-stocks-"+datetime.now().strftime("%d-%m-%Y")+".csv"
    gname = "NSE-upcoming-Dividend-"+datetime.now().strftime("%d-%m-%Y")+".csv"

    f = open('static/'+fname,'a')
    f.write("Company name,Purpose,Ex-dividend Date,Dividend Yield,Dividend,Base Price\r\n")
    g = open('static'+gname,'a')
    g.write("Company name,Ex-dividend Date,Dividend Yield,Dividend,Base Price,Upcoming\r\n")

    # calling to nse API
    # stock_codes = nse.get_stock_codes(cached=False)
    stock_codes = nse.get_stock_codes()

    count = 0
    totalStocks = len(stock_codes)
    for key in stock_codes.keys():
        count +=1
        try:
            quote = nse.get_quote(key)
            sleep(0.01)
            purpose = quote.get('purpose')
            companyName =quote.get('companyName')
            basePrice = str(quote.get('basePrice'))
            exDividendDate = quote.get('exDate')
            divPurpose = Utilis.getPurpose(purpose)
            if divPurpose:
                dividend = Utilis.dividendMatch(purpose,ptn)
                dividendYield = Utilis.divYield(dividend,basePrice)
                upcoming = Utilis.findUpcomingDividend(exDividendDate)
                terminalOutput(count,totalStocks,key,companyName,purpose,dividend,exDividendDate,dividendYield,basePrice,upcoming)
                fileOutput(f,g,companyName,purpose,exDividendDate,dividendYield,dividend,basePrice,upcoming)
        except IndexError:
            print("Index Error...")
        except ValueError:
            print("Value Error...")
    f.close()
    g.close()

if __name__ == "__main__":
    dividend(nse,ptn)

# Todos:
# 3. Sort according to dividend yield
# 4. make in interactive to terminal,takes file name gives option to choose output destination.
# 5. store all the gathered info in a database
# 6. import os,sys module to make terminal output more fancy
# 7. Delete <2% dividend and dividend before 2021