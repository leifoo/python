import sys
from datetime import datetime
from selenium import webdriver

now = datetime.now()
date = now.strftime("%Y-%b-%d")
print(date)

url = "https://www.nasdaq.com/dividend-stocks/dividend-calendar.aspx?date=2019-Sep-16"

class dividend:
    def __init__(self, exDivDate, company, div, annualDiv, recordDate, announceDate, payDate):
        self.exDivDate = exDivDate
        self.company = company
        self.div = div
        self.annualDiv = annualDiv
        self.recordDate = recordDate
        self.announceDate = announceDate
        self.payDate = payDate

driver = webdriver.Chrome()
#driver.get("https://www.nasdaq.com/dividend-stocks/dividend-calendar.aspx?date=2019-Sep-16")
driver.get('file://' + "/Users/chen/Downloads/Dividend_Calendar.htm")
#table = driver.find_elements_by_class_name("DividendCalendar")
table = driver.find_element_by_class_name("DividendCalendar")

tablehead = table.find_element_by_tag_name('thead')
tablebody = table.find_element_by_tag_name('tbody')

tablecolomnname  = tablehead.find_elements_by_tag_name('th')

#print(tableheading.text.strip())

if len(tablecolomnname) != 7:
    sys.exit('Table column changed!!!')

dividendIndex = -sys.maxsize

for i,column in enumerate(tablecolomnname):
    if column.text.strip() == 'Dividend':
        dividendIndex = i
        print(i, column.text.strip())
        break

if dividendIndex == -sys.maxsize:
    sys.exit('Table without Dividened column???')

tablerow = tablebody.find_elements_by_tag_name('tr')

for row in tablerow:
    dataset = row.find_elements_by_tag_name('td')

    print(dataset[dividendIndex].text.strip())

driver.close()
