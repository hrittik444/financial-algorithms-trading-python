#%%
import pandas as pd
import pandas_datareader as web
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')

# we can almost treat CAPM as a simple linear regression
# stats.linregress calculates linear regression using least squares, with some x and y value
help(stats.linregress)

start = pd.to_datetime('2010-01-04')
end = pd.to_datetime('2017-07-18')

# using pandas datareader to fetch data about the SPY S&P500 ETF using the yahoo api
spy_etf = web.DataReader('SPY','yahoo',start,end)
spy_etf.info()
spy_etf.head()

# say our portfolio strategy is to completely invest in Apple stock

# using pandas datareader to fetch data about Apple stock
aapl = web.DataReader('AAPL','yahoo',start,end)
aapl.head()

# plotting Close Price of AAPL vs. SPY
aapl['Close'].plot(label='AAPL',figsize=(10,8))
spy_etf['Close'].plot(label='SPY Index')
plt.legend()

# comparing Cumulative Return of AAPL and SPY 
aapl['Cumulative'] = aapl['Close']/aapl['Close'].iloc[0]
spy_etf['Cumulative'] = spy_etf['Close']/spy_etf['Close'].iloc[0]

# plotting Cumulative Return of AAPL vs. SPY
aapl['Cumulative'].plot(label='AAPL',figsize=(10,8))
spy_etf['Cumulative'].plot(label='SPY Index')
plt.legend()
plt.title('Cumulative Return')

# comparing Daily Return of AAPL and SPY 
aapl['Daily Return'] = aapl['Close'].pct_change(1)
spy_etf['Daily Return'] = spy_etf['Close'].pct_change(1)

# plotting Daily Return of AAPL vs. SPY
plt.scatter(aapl['Daily Return'],spy_etf['Daily Return'],alpha=0.3)
aapl['Daily Return'].hist(bins=100)
spy_etf['Daily Return'].hist(bins=100)


## using the linregress function to obtain alpha and beta values
# using the index 1 and onwards, since we cannot pass in null values (the first value in the Daily Returns column is null)
beta,alpha,r_value,p_value,std_err = stats.linregress(aapl['Daily Return'].iloc[1:],spy_etf['Daily Return'].iloc[1:])
print(beta)
print(alpha)


## testing the CAPM model
# what if our stock was completely in line with the S&P500?
# in that case, we would expect t see a really high beta value
# so we are going to generate some artificial noise for our stock data
# and then try to get it lined up with the S&P500
# and see if we get a higher beta value
# that will confirm for sure that the CAPM model is working as expected

# gives a normally distributed random values (specifying mean as 0 and std dev. as 0.001)
noise = np.random.normal(0,0.001,len(spy_etf['Daily Return'].iloc[1:]))
print(noise)

# adding the noise to the Daily Return values
spy_etf['Daily Return'].iloc[1:] + noise

# using the linregress function to obtain alpha and beta values
beta,alpha,r_value,p_value,std_err = stats.linregress(spy_etf['Daily Return'].iloc[1:]+noise,spy_etf['Daily Return'].iloc[1:])

# we see a very high beta value, almost 1
print(beta)
print(alpha)

# so our CAPM model is working correctly