import pandas as pd
# run pip install quandl
import quandl
import matplotlib.pyplot as plt


# Creating a Portfolio
# hardcoding start date (1st Jan 2012) and end date (1st Jan 2017)
start = pd.to_datetime('2012-01-01')
end = pd.to_datetime('2017-01-01')

# Grabbing Apple, Cisco, IBM and Amazon Stock data from Quandl for our portfolio
aapl = quandl.get('WIKI/AAPL.11', start_date=start, end_date=end)
csco = quandl.get('WIKI/CSCO.11', start_date=start, end_date=end)
ibm = quandl.get('WIKI/IBM.11', start_dat=start, end_date=end)
amzn = quandl.get('WIKI/IBM.11', start_dat=start, end_date=end)

# Alternatively, can use the provided sample CSV files in case problems arise with quandl 
# aapl = pd.read_csv('AAPL_CLOSE', index_col='Date', parse_dates=True)
# csco = pd.read_csv('CISCO_CLOSE', index_col='Date', parse_dates=True)
# ibm = pd.read_csv('IBM_CLOSE', index_col='Date', parse_dates=True)
# amzn = pd.read_csv('AMZN_CLOSE', index_col='Date', parse_dates=True)

aapl.to_csv('AAPL_CLOSE')
csco.to_csv('CISCO_CLOSE')
ibm.to_csv('IBM_CLOSE')
amzn.to_csv('AMZN_CLOSE')

# Normalizing prices (ie: calculating Cumulative Returns)
for stock_df in [aapl,csco,ibm,amzn]:
    stock_df['Normalized Return'] = stock_df['Adj. Close']/stock_df.iloc[0]['Adj. Close']

# Say portfolio comprises of the following allocations:
# 30% in Apple
# 20% in Cisco
# 40% in IBM
# 10% in Amazon
for stock_df,allocation in zip([aapl,csco,ibm,amzn],[0.3,0.2,0.4,0.1]):
    stock_df['Allocation'] = stock_df['Normalized Return']*allocation

# Say $1,000,000 was invested in this portfolio, calculating the Position Value
for stock_df in [aapl,csco,ibm,amzn]:
    stock_df['Position Value'] = stock_df['Allocation']*1000000

# calculating Total Portfolio Value for each stock:
portfolio_val = pd.concat([aapl['Position Value'],csco['Position Value'],ibm['Position Value'],amzn['Position Value']], axis=1)
portfolio_val.columns = ['Apple Position Value','Cisco Position Value','IBM Position Value','Amazon Position Value']

# calculating Total Position
portfolio_val['Total Position'] = portfolio_val.sum(axis=1)

# Plotting the Total Portfolio Value and Total Position using matplotlib
portfolio_val.drop('Total Position', axis=1).plot(figsize=(10,8),title='Total Portfolio Value')
portfolio_val['Total Position'].plot(figsize=(10,8),title='Total Position')

# Daily Return
portfolio_val['Daily Return'] = portfolio_val['Total Position'].pct_change(1)

# Mean of Daily Return
average_daily_return = portfolio_val['Daily Return'].mean()

# Std Deviation of Daily Return
std_daily_return = portfolio_val['Daily Return'].std()

# Plotting Daily Return as Kernel Density Plot and Histogram
portfolio_val['Daily Return'].plot(kind='kde', figsize=(4,5))
portfolio_val['Daily Return'].plot(kind='hist', figsize=(4,5))

# Overall Cumulative Return (over the entire specified time period)
cumulative_return = 100 * (portfolio_val['Total Position'][-1]/portfolio_val['Total Position'][0] -1 )

# ----------------------------------------------------------------------------------------------------------
# Using Sharpe Ratio for calculating risk-adjusted return
# Sharpe ratio = (Mean portfolio return − Risk-free rate)/Standard deviation of portfolio return
# Annual Sharpe Ratio = K-value * Sharpe Ratio
    # when data is daily, K-value = sqrt(252)
    # when data is weekly, K-value = sqrt(52)
    # when data is monthly, K-value = sqrt(12)
# for the purpose of this example, we are considering Risk-free rate in the US as Zero
# the higher the Sharpe Ratio, the better the portfolio
# for a different country, the Daily Rate can be calculated using the below formula, givent the Yearly Rate
    # daily_rate = ((1.0 + yearly_rate)**(1/252))-1

sharpe_ratio = portfolio_val['Daily Return'].mean()/portfolio_val['Daily Return'].std()
annual_sharpe_ratio = (252**0.5)*sharpe_ratio
portfolio_val.head()