import argparse
import bs4 as bs
import datetime as dt
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import style
import os
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests
import time
from tqdm import tqdm # progress
import sys

style.use('ggplot')
mpl.rcParams['figure.figsize'] = (16.0, 9.0)
# mpl.rcParams['font.size'] = 12
# mpl.rcParams['legend.fontsize'] = 'large'
# mpl.rcParams['figure.titlesize'] = 'medium'

default_start_year = 2010
data_path = '../data/all_stock'
useLocalData = False

parser = argparse.ArgumentParser(description='Compare stocks')
parser.add_argument('symbol', nargs='+', type=str,
                   help='Stock symbols')
parser.add_argument('-d', '--date', nargs='+', type=str,
                   help='Start date and end date (default: '+str(default_start_year)+'0101 to today)')
parser.add_argument('-n', '--norm', nargs=1, type=str,
                   help='Normalize to 1 on start date (y/n, default is y')
parser.add_argument('-l', '--local', nargs=1, type=str,
                   help='Use local stored dataset (y/n, default is n')

args = parser.parse_args()
# print(args.date, args.symbol)
# print(parser.parse_args('-s XOM -d 20200518'.split()))
# print(parser.parse_args('--symbol XOM AAPL --date 20200518 20200519'.split()))

# Use local data
if args.local:
    if args.local[0] == 'y':
        useLocalData = True
    elif args.local[0] != 'n':
        sys.exit('Error: Use local stored dateset choice y/n!')

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

tickers = args.symbol
main_df = pd.DataFrame()

ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1,sharex=ax1)

for count, ticker in enumerate(tqdm(tickers)):
    # ticker = ticker.lstrip().rstrip().replace('~', '')
    print(count, ticker)

    if useLocalData:
        useLocalData = os.path.exists(data_path+'/{}.csv'.format(ticker))

    if useLocalData:
        print('Retrieve data from '+data_path+'/{}.csv'.format(ticker))
        df = pd.read_csv(data_path+'/{}.csv'.format(ticker))
    else:
        print('Retrieve data from Yahoo...')
        try:
            df = web.DataReader(ticker, 'yahoo', start, end)
        except:
            print(ticker, 'does not exist! Skip...')
            continue

    # print(df.tail())
    # time.sleep(0.5)

    if not useLocalData:
        df.reset_index(inplace=True)
    
    df.set_index("Date", inplace=True)

    df.rename(columns={'Adj Close': ticker, 'Volume': ticker+'_volume'}, inplace=True)
    if not useLocalData:
        df.drop(['Open', 'High', 'Low', 'Close'], 1, inplace=True)
    else:
        # print(df.index)
        df.index = pd.to_datetime(df.index, format='%Y-%m-%d')
        # print(df.index, df.columns)
        df = df[(df.index >= start) & (df.index <= end)]

    if main_df.empty:
        main_df = df
    else:
        main_df = main_df.join(df, how='outer')

    # Normalize to 1 at start date
    if not args.norm or args.norm[0] == 'y':
        # print(df.iloc[0, 0], df.iloc[1, 0], df.iloc[0, 1], df.iloc[1, 1])
        main_df[ticker] /= df.iloc[0, 1]
        ax1.text(main_df.index[-1], main_df[ticker][-1], "%.3f" %main_df[ticker][-1], va="bottom", ha="left", fontsize=12)

    ax1.plot(main_df.index, main_df[ticker], label=ticker)
    ax2.plot(main_df.index, main_df[ticker+'_volume'], label=ticker+'_volume')

ax1.legend(loc='upper left')
ax1.set(xlabel='', ylabel = 'Adjusted Close Price')
ax1.xaxis.set_tick_params(labeltop=True, labelbottom=False)
ax2.legend(loc='upper left')
ax2.set(xlabel=df.index.name, ylabel='Volume')
plt.show()