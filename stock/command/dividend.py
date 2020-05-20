from pandas_datareader import data as pdr

import yfinance as yf
yf.pdr_override()

msft = yf.Ticker("MSFT")

# get stock info
msft.info

# get historical market data
hist = msft.history(period="max")

# show actions (dividends, splits)
msft.actions

# show dividends
print(msft.dividends)
print(yf.Ticker("XOM").dividends)