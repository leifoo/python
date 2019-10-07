import sys
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

now = datetime.now()
date = now.strftime("%Y-%b-%d")
print(date)

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

# Headless version
chrome_options = Options()  
chrome_options.add_argument("--headless")
chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
#chrome_options.binary_location = '/Applications/Google Chrome   Canary.app/Contents/MacOS/Google Chrome Canary'
driver = webdriver.Chrome(chrome_options=chrome_options)

# Virtually open a browser
# driver = webdriver.Chrome()

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

for i,row in enumerate(tablerow):
    dataset = row.find_elements_by_tag_name('td')

    print(dataset[0].text.strip(), dataset[dividendIndex-1].text.strip())

    if i == len(tablerow)-1:
        driver.get(stockurl+dataset[0].text.strip())

#if driver.find_element_by_class_name("pagination__next"):
#    driver.find_element_by_class_name("pagination__next").click()

driver.close()
