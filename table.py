from datetime import date,datetime
from backend.getdata import getAllData
from backend.analysis import analyzeAll
from terminaltables import AsciiTable



dfs = getAllData()
op = analyzeAll(dfs,['rsi','macd','stoch'])

def printTable(op):
    tdate = datetime.date(datetime.now())
    data = [['\033[0;37m Date \033[0m','\033[0;37m Name \033[0m','\033[0;37m Indicator \033[0m','\033[0;37m Value \033[0m','\033[0;37m Price \033[0m','\033[0;37m Advice \033[0m']]
    for i in op:
        for val in i:
            for i,v in val.iterrows():
                if v['date'] == str(tdate):
                    z = v.to_list()
                    y = []
                    if v['adv'] == "BUY":
                        for j in z:
                            fj = "\033[0;93m {0} \033[0m".format(j)
                            y.append(fj)
                    elif v['adv'] == "SELL":
                        for j in z:
                            fj = "\033[0;36m {0} \033[0m".format(j)
                            y.append(fj)
                    # data.append(v.to_list())
                    data.append(y)
    table = AsciiTable(data)
    print(table.table)

printTable(op)













# nse = Nse()

# sc = nse.get_stock_codes()

# with open('static/stocks.csv','w') as f:
#     w = csv.writer(f)
#     for i,v in sc.items():
#         w.writerow([i,v])
