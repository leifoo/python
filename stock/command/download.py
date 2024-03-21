# +
# conda install -c anaconda pandas-datareader
# conda install -c conda-forge tqdm
# sudo pip install get-all-tickers
# -

import argparse
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import time
from tqdm import tqdm # progress
import sys
from get_all_tickers import get_tickers as gt
import requests
import bs4 as bs
import yfinance as yf
yf.pdr_override()

default_start_year = 2000
data_path = '../data/all_stock'

# reserved name in Windows
reserved = ['PRN']

parser = argparse.ArgumentParser(description='Compare stocks')
parser.add_argument('-s', '--symbol', nargs='+', type=str,
                   help='Stock symbols; Default empty, download all')
parser.add_argument('-d', '--date', nargs='+', type=str,
                   help='Start date and end date (default: '+str(default_start_year)+'0101 to today)')
parser.add_argument('-a', '--all', nargs=1, type=str,
                   help='Download all price (Adj Close, Open, High, Low, Close) or only Adj Close (y/n, default is n')

args = parser.parse_args()
# print(args.date, args.symbol)
# print(parser.parse_args('-s XOM -d 20200518'.split()))
# print(parser.parse_args('--symbol XOM AAPL --date 20200518 20200519'.split()))

# Load data
start = dt.datetime(default_start_year, 1, 1)
if args.date:
    month, day = 1, 1
    len_start = len(args.date[0])
    if len_start == 6:
        month = int(args.date[0][4:6])
    elif len_start == 8:
        day = int(args.date[0][6:8])
    elif len_start != 4:
        sys.exit('Error: Start date format -d 2020[12][31]')
    start = dt.datetime(int(args.date[0][:4]), month, day)

end = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
if args.date and len(args.date) == 2:
    month, day = 1, 1
    len_start = len(args.date[1])
    if len_start == 6:
        month = int(args.date[1][4:6])
    elif len_start == 8:
        day = int(args.date[1][6:8])
    elif len_start != 4:
        sys.exit('Error: End date format -d 2020[12][31]')
    end = dt.datetime(int(args.date[1][:4]), month, day)

print('Start date:', start)
print('  End date:', end)


# +
def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker.rstrip().replace('.', '-'))
        
#     with open("sp500tickers.pickle","wb") as f:
#         pickle.dump(tickers,f)
        
    print('Total number of tickers: ', len(tickers))
    return tickers


# -

if args.symbol:
    tickers = args.symbol
else:
#     tickers = gt.get_tickers()
    tickers = save_sp500_tickers()[:]

print('Number of tickers: ', len(tickers))
print('Last 5 tickers: ', tickers[-5:])

# Add data path
if not os.path.exists(data_path):
    print(data_path, ' does not exist, create it now...')
    os.makedirs(data_path)

missing_ticker =[]

# Download
for count, ticker in enumerate(tqdm(tickers)):
    ticker = ticker.lstrip().rstrip().replace('~', '').replace('$', '')
    # print(count, ticker)

    if not os.path.exists(data_path+'/{}.csv'.format(ticker)):
        try:
            df = web.get_data_yahoo(ticker, start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))
        except:
            print(ticker, 'does not exist! Skip...')
            missing_ticker.append(ticker)
            continue

        print(df)
        # time.sleep(0.5)
        if not args.all:
            df.drop(['Open', 'High', 'Low', 'Close'], inplace=True)

        if ticker in reserved:
            ticker += '_' 
            
        fullname = os.path.join(data_path, ticker+'.csv')
        df.to_csv(fullname)
    else:
        print('Already have {}'.format(ticker))

print('Missing ticker:\n ', missing_ticker)
