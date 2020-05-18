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

style.use('ggplot')
mpl.rcParams['figure.figsize'] = (16.0, 9.0)
mpl.rcParams['font.size'] = 12
# mpl.rcParams['legend.fontsize'] = 'large'
mpl.rcParams['figure.titlesize'] = 'medium'

parser = argparse.ArgumentParser(description='Compare stocks')
parser.add_argument('symbol', nargs='+', type=str,
                   help='Stock symbols')
parser.add_argument('-d', '--date', nargs='+', type=str,
                   help='Start date and end date (optional)')

args = parser.parse_args()
# print(args.date, args.symbol)
# print(parser.parse_args('-s XOM -d 20200518'.split()))
# print(parser.parse_args('--symbol XOM AAPL --date 20200518 20200519'.split()))

# Load data
start = dt.datetime(int(args.date[0][:4]), int(args.date[0][4:6]), int(args.date[0][6:8]))
end = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
if len(args.date) == 2:
    end = dt.datetime(int(args.date[1][:4]), int(args.date[1][4:6]), int(args.date[1][6:8]))
print('Start date:', start)
print('  End date:', end)

tickers = args.symbol
main_df = pd.DataFrame()

ax1 = plt.subplot2grid((6,1), (0,0), rowspan=4, colspan=1)
ax2 = plt.subplot2grid((6,1), (4,0), rowspan=2, colspan=1,sharex=ax1)

for count, ticker in enumerate(tqdm(tickers)):
    df = web.DataReader(ticker, 'yahoo', start, end)
    print(df.tail())
#        time.sleep(0.5)
    df.reset_index(inplace=True)
    df.set_index("Date", inplace=True)
   # df.to_csv('stock_dfs/{}.csv'.format(ticker))
   # df.set_index('Date', inplace=True)

    df.rename(columns={'Adj Close': ticker, 'Volume': ticker+'_volume'}, inplace=True)
    df.drop(['Open', 'High', 'Low', 'Close'], 1, inplace=True)

    if main_df.empty:
        main_df = df
    else:
        main_df = main_df.join(df, how='outer')

    print(main_df.tail())
    ax1.plot(main_df.index, main_df[ticker], label=ticker)
    ax2.plot(main_df.index, main_df[ticker+'_volume'], label=ticker+'_volume')

ax1.legend(loc='upper left')
ax1.set(xlabel='', ylabel = 'Adjusted Close Price')
ax1.xaxis.set_tick_params(labeltop=True, labelbottom=False)
ax2.legend(loc='upper left')
ax2.set(xlabel=df.index.name, ylabel='Volume')
plt.show()