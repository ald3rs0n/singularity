import requests
from bs4 import BeautifulSoup
from pprint import pprint
from terminaltables import AsciiTable
import html_to_json

#  https://www.topstockresearch.com/rt/AutoComplete.tsr?ex=in&eqSubCat=Fundamental&term=adaniport
# https://www.topstockresearch.com/rt/AutoComplete.tsr?ex=in&eqSubCat=All&term=adaniport

# https://www.topstockresearch.com/INDIAN_STOCKS/MINING/FundamentalAnalysisOfVedanta_Ltd.html

# https://www.topstockresearch.com/INDIAN_STOCKS/REFINERIES/Reliance_Industries_Ltd.html

# https://www.topstockresearch.com/INDIAN_STOCKS/BANKS/HDFC_Bank_Ltd.html

# https://www.topstockresearch.com/INDIAN_STOCKS/PHARMACEUTICALS/FundamentalAnalysisOfSanofi_India_Ltd.html

# https://www.topstockresearch.com/INDIAN_STOCKS/COMPUTERS_SOFTWARE/FundamentalAnalysisOfLatent_View_Analytics_Ltd.html




ex = "in"
eqSubCat = "Fundamental" # All
# term = "adaniports"

def get_fundamentals(symbol,ex="in",eqSubCat="Fundamental"):
    url = f"https://www.topstockresearch.com/rt/AutoComplete.tsr?ex={ex}&eqSubCat={eqSubCat}&term={symbol}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }
    headers2 ={
    'Host': 'www.topstockresearch.com',
    'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://www.topstockresearch.com/INDIAN_STOCKS/BANKS/FundamentalAnalysisOfIndustrial_Development_Bank_of_India_Ltd.html',
    'Cookie': 'utma=211277200.990350735.1650549195.1650549195.1650549195.1; __utmb=211277200.29.10.1650549195; __utmc=211277200; __utmz=211277200.1650549195.1.1.utmcsr=duckduckgo.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __gads=ID=0b97971e54126cd3-221a1c025bd20023:T=1650548873:RT=1650549551:S=ALNI_MZgwc-77WYmMG7u0VMIQk0vYe3p9A; __gpi=UID=000004f5f11fbcb2:T=1650549522:RT=1650549522:S=ALNI_MagqpQ_3SNoVjvdEkjBB-oV5t-4WA; __utmt=1',
    'Upgrade-Insecure-Requests': '1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
    }

    r = requests.get(url,headers)
    link = r.json()[0]['id']
    r2 = requests.get(url=link,headers=headers2)
    soup = BeautifulSoup(r2.content,'html.parser')

    all_tables = soup.find_all('div',class_='table-responsive')
    company_details = soup.find('div', style="border: 1.25px solid  #84a981;border-radius:5px;border-color: #84a981;margin:4px;padding:4px; text-align:justify")
    fundamentals = {'Symbol' : symbol}
    # print(company_details)
    fundamentals['Details'] = company_details.contents[4]
    fundamentals['Link'] = company_details.contents[12]

    for tables in all_tables:
        if str(tables) >= str(all_tables[3]):
            table = html_to_json.convert_tables(str(tables))
            try:
                for item in table[0]:
                    fundamentals[item[0]] = item[1].replace("\xa0","")
            except IndexError:
                pass


    terrific_view = html_to_json.convert_tables(str(all_tables[0]))[0][0]
    stedy_view = html_to_json.convert_tables(str(all_tables[1]))[0][0]
    risky_view = html_to_json.convert_tables(str(all_tables[2]))[0][0]
    return fundamentals

    # highlights = html_to_json.convert_tables(str(all_tables[3]))
    # overview = html_to_json.convert_tables(str(s[4]))

    # values = html_to_json.convert_tables(str(s[6])) 
    # mqr = html_to_json.convert_tables(str(s[7])) 
    # ttm = html_to_json.convert_tables(str(s[8])) 

    # valuation = html_to_json.convert_tables(str(s[9])) 
    # profitabilities = html_to_json.convert_tables(str(s[10])) 

    # solvency = html_to_json.convert_tables(str(s[11])) 
    # efficiency = html_to_json.convert_tables(str(s[12])) 

    # balance_sheet = html_to_json.convert_tables(str(s[13])) 
    # cash_flow = html_to_json.convert_tables(str(s[14])) 

    # annual_income = html_to_json.convert_tables(str(s[15])) 
    # quartly_income = html_to_json.convert_tables(str(s[16])) 



f = get_fundamentals('ioc')
pprint(f)