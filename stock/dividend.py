import sys
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import yfinance as yf

now = datetime.now()
date = now.strftime("%Y-%b-%d")
print(date)

headless = False
url = "https://www.nasdaq.com/market-activity/dividends"
stockurl = "https://www.nasdaq.com/market-activity/stocks/"
tablename = "market-calendar-table__table"
numberofcolumn = 8
dividendname = 'DIVIDEND'

class dividend:
    def __init__(self, exDivDate, company, div, annualDiv, recordDate, announceDate, payDate):
        self.exDivDate = exDivDate
        self.company = company
        self.div = div
        self.annualDiv = annualDiv
        self.recordDate = recordDate
        self.announceDate = announceDate
        self.payDate = payDate

chrome_options = Options()
if headless: 
    # Headless version  
    chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)

# driver = webdriver.Chrome('./chromedriver')
# chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
# chrome_options.binary_location = '/Applications/Google Chrome   Canary.app/Contents/MacOS/Google Chrome Canary'



driver.get(url)
#driver.get('file://' + "/Users/chen/Downloads/Dividend_Calendar.htm")

table = driver.find_element_by_class_name(tablename)

tablehead = table.find_element_by_tag_name('thead')
tablebody = table.find_element_by_tag_name('tbody')

tablecolomnname  = tablehead.find_elements_by_tag_name('th')

if len(tablecolomnname) != numberofcolumn:
    sys.exit('Table column changed!!!')

dividendIndex = -sys.maxsize

for i,column in enumerate(tablecolomnname):
    if column.text.strip() == dividendname:
        dividendIndex = i
        print(i, column.text.strip())
        break

if dividendIndex == -sys.maxsize:
    sys.exit('Table without Dividened column???')

tablerow = tablebody.find_elements_by_tag_name('tr')
print( 'Number of rows = ', len(tablerow) )

for i,row in enumerate(tablerow):
    dataset = row.find_elements_by_tag_name('td')

    stock_symbol = dataset[0].text.strip()
    ticker = yf.Ticker(stock_symbol)
    today_price = ticker.history().tail(1)
    dividend_amount = float(dataset[dividendIndex-1].text.strip())
    print(stock_symbol, today_price.columns[0], today_price['Close'], dividend_amount) # dividend_amount / today_price['Close'] * 100, '%')


    if i == len(tablerow)-1:
        driver.get(stockurl+dataset[0].text.strip())
        # today_price = driver.find_element_by_class_name('symbol-page-header__pricing-price')
        # print( 'Today price', today_price.text.strip())

#if driver.find_element_by_class_name("pagination__next"):
#    driver.find_element_by_class_name("pagination__next").click()

# driver.close()
