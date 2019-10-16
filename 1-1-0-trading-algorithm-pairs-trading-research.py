#%%
## Pairs Trading: a trading strategy that involves matching a long position with a short position in two stocks that are highly correlated

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import quandl

start = '07-01-2015'
end = '07-01-2017'

united = quandl.get('WIKI/UAL',start_date=start,end_date=end)
american = quandl.get('WIKI/AAL',start_date=start,end_date=end)

print(united.head())
print(american.head())

american['Adj. Close'].plot(label='American Airlines',figsize=(12,8))
united['Adj. Close'].plot(label='United Airlines')
plt.legend()

# getting the correlation coeff between our two assets
np.corrcoef(american['Adj. Close'],united['Adj. Close'])

# so we see that they are highly correlated with each other
# due to this, we are gonna make the following assumption in our trading strategy:
# "any significant differences in the spread of their prices, may be a trading opportunity"

# calculating and plotting the spread
spread = american['Adj. Close'] - united['Adj. Close']
spread.plot(label='Spread',figsize=(12,8))
# marking a red horizontal line along the average spread
plt.axhline(spread.mean(),c='r')
plt.legend()


## normalizing with a z-score:
# normalizing the prices of the two stocks with z-score
# sorta like bringing the two stocks toether so we can trade them both in association with each other
def zscore(stocks):
    return (stocks - stocks.mean()) / np.std(stocks)

# plotting the normalized spread
zscore(spread).plot(figsize=(14,8))
plt.axhline(zscore(spread).mean(), color='black')
plt.axhline(1.0, c='r', ls='--')
plt.axhline(-1.0, c='g', ls='--')
plt.legend(['Spread z-score', 'Mean', '+1', '-1']);

# the black line represents the normalized average spread and is at 0.0
# the red and green lines are 1.0 points above and below the average spread
# so we can devise our strategy around these as the upper and lower limits, and if the spread crosses either of these ...take some action (long/short) etc.

# for the purpose of this example, our strategy will be as follows:
    # "if there is ever a rise over 0.5 or dip below -0.5... 
    # ...then I expect there to be a 'Reversion to the Mean'"
    # ie: since the stocks are highly correlated, therefore eventually the spread (blue line) will dip back down or rise back up to the normalized average spread


## normalizing with a rolling z-Score:
# when implementing this in Quantopian, 
# during a backtest, we will not be having immediate access to the entire dataframe for the stocks
# so we need to be able to calculate a rolling version of the z-score

# 1 day moving average of the price spread
spread_mavg1 = spread.rolling(1).mean()

# 30 day moving average of the price spread
spread_mavg30 = spread.rolling(30).mean()

# rolling 30 day standard deviation
std_30 = spread.rolling(30).std()

# computing the z score for each day
zscore_30_1 = (spread_mavg1 - spread_mavg30)/std_30

# plotting the spread
zscore_30_1.plot(figsize=(12,8),label='Rolling 30 day Z score')
plt.axhline(0, color='black')
plt.axhline(0.5, color='red', linestyle='--')
plt.axhline(-0.5, c='green', linestyle='--')