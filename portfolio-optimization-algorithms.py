## finding Optimal Portfolio using the Monte Carlo Simulation to randomly allocate weights and compute the best Sharpe Ratio

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

# Download and get Daily Returns
aapl = pd.read_csv('AAPL_CLOSE', index_col='Date', parse_dates=True)
csco = pd.read_csv('CISCO_CLOSE', index_col='Date', parse_dates=True)
ibm = pd.read_csv('IBM_CLOSE', index_col='Date', parse_dates=True)
amzn = pd.read_csv('AMZN_CLOSE', index_col='Date', parse_dates=True)

# creating our consolidated Stocks dataframe from above data
stocks = pd.concat([aapl,csco,ibm,amzn], axis=1)
stocks.columns = ['Apple', 'Cisco', 'IBM', 'Amazon']

# Mean Daily Return
daily_return = stocks.pct_change(1)
mean_daily_return = stocks.pct_change(1).mean()

# correlation coeff between the Daily Returns
corr_daily_return = stocks.pct_change(1).corr()

# we shall use logarithmic returns instead of arithmetic returns, going forward
# further reading: https://quantivity.wordpress.com/2011/02/21/why-log-returns/

# Logarithmic Daily Return
log_return = np.log(stocks/stocks.shift(1))

# plotting Logarithmic Daily Returns
log_return.hist(bins=100, figsize=(12,8))
plt.tight_layout()

# Logarithmic Mean Daily Return
mean_log_return = log_return.mean()

# correlation coeff between the Logarithmic Daily Returns
corr_log_return = log_return.corr()

# covariance between the Logarithmic Daily Returns
cov_log_return = log_return.cov()

## algorithm for a single run of random allocation
# creating random weights
print('Creating Random Weights')
weights = np.array(np.random.random(4))
print(weights)
print('\n')

# rebalancing weights (making sure random weights add up to 1.0 ...this is actually a common normalization technique)
print('Rebalance Random Weights to sum to 1.0')
weights = weights / np.sum(weights)
print(weights)
print('\n')

# Expected Return
# the numerator of sharpe ratio
print('Expected Portfolio Return')
expected_return = np.sum(log_return.mean() * weights) *252
print(expected_return)
print('\n')

# Expected Variance/Volatility
# the denominator of sharpe ratio
print('Expected Volatility')
expected_volatility = np.sqrt(np.dot(weights.T, np.dot(log_return.cov() * 252, weights)))
print(expected_volatility)
print('\n')

# Volatility is the up-and-down change in the price or value of an individual stock or the overall market during a given period of time. Volatility can be measured by comparing current or expected returns against the stock or market’s mean (average)
# source: https://www.ally.com/do-it-right/investing/what-is-volatility-and-how-to-calculate-it/

# Sharpe Ratio
sharpe_ratio = expected_return/expected_volatility
print('Sharpe Ratio')
print(SR)

## running the same algorithm for mltiple random allocations for many portfolio cases
# say we wanna consider 5000 portfolios  
num_portfolios = 15000

weights_arr = np.zeros((num_portfolios,len(stocks.columns)))
return_arr = np.zeros(num_portfolios)
volatility_arr = np.zeros(num_portfolios)
sharpe_ratio_arr = np.zeros(num_portfolios)

for i in range(num_portfolios):
    
    # creating random weights
    weights = np.array(np.random.random(4))
    
    # rebalancing weights
    weights = weights / np.sum(weights)
    
    # save the random weights to weights array (using broadcasting)
    weights_arr[i,:] = weights
    
    # Expected Return
    return_arr[i] = np.sum((log_return.mean()*weights) * 252) 
    
    # Expected Variance/Volatility
    volatility_arr[i] = np.sqrt(np.dot(weights.T, np.dot(log_return.cov()*252, weights)))
    
    # Sharpe Ratio
    sharpe_ratio_arr[i] = return_arr[i]/volatility_arr[i]

# Maximum Sharpe Ratio obtained
max_sharpe_ratio = sharpe_ratio_arr.max()

# index location of the Maximum Sharpe Ratio obtained
index_max_sharpe_ratio = sharpe_ratio_arr.argmax()

# Optimal Allocation (at Maximum Sharpe Ratio)
weights_arr[index_max_sharpe_ratio,:]

# Expected Return and Volatility at Maximum Sharpe Ratio
max_sr_return = return_arr[index_max_sharpe_ratio]
max_sr_volatility = volatility_arr[index_max_sharpe_ratio]

# plotting the data
plt.figure(figsize=(12,8))
plt.scatter(volatility_arr,return_arr,c=sharpe_ratio_arr)
plt.colorbar(label='Sharpe Ratio')
plt.xlabel('Volatility')
plt.ylabel('Return')
plt.show()

# marking the point of Maximum Sharpe Ratio on plot
plt.scatter(max_sr_volatility,max_sr_return,c='red',s=90,edgecolors='black')


## ----------------------------------------------------------------------------------------------
## finding Optimal Portfolio mathematically using SciPy

# functionalizing the Return, Volatility and Sharpe Ratio operations
def ret_vol_sr(weights):
    """
    Takes in weights, returns an array containing return, volatility and sharpe ratio
    """
    weights = np.array(weights)
    ret = np.sum((log_return.mean()*weights) * 252)
    vol = np.sqrt(np.dot(weights.T, np.dot(log_return.cov()*252, weights)))
    sr = ret/vol
    return np.array([ret,vol,sr])

# function for minimizing the Negative Sharpe Ratio (ie: maximizing the Positive Sharpe Ratio)
def min_neg_sr(weights):
    return ret_vol_sr(weights)[2] * -1

# constraints
def check_sum(weights):
    """
    Returns 0 if sum of weights is 1.0
    """
    return np.sum(weights) - 1

# By convention of minimize function it should be a function that returns zero for conditions
constraints = ({'type':'eq', 'fun':check_sum}) 

# setting 0-1 bounds for weights
bounds = ((0, 1), (0, 1), (0, 1), (0, 1))

# initial guess for allocation (equal distribution)
initial_guess = [0.25,0.25,0.25,0.25]

# Minimizing using SciPy Sequential Least SQuares Programming (SLSQP) algorithm
optimal_results = minimize(min_neg_sr, initial_guess, method='SLSQP', bounds=bounds, constraints=constraints)

# Optimal Allocation
optimal_allocation = optimal_results.x

# using the weights obtained from Optimal Allocation 
# and passing it to our function to find Daily Returns, Volatility and Sharpe Ratio
results = ret_vol_sr(optimal_results.x)


## calculating Effecient Frontier to determine the highest expected return for a defined level of risk or the lowest risk for a given level of expected return
## portfolios below the Effecient Frontier curve are considered sub-optimal

# plot had Return on y axis and Volatility on x axis
# frontier_y is an array of equally spaced values of Returns between 0 to 0.3
frontier_y = np.linspace(0,0.3,100)

# function for minimizing volatility
def min_vol(weights):
    return ret_vol_sr(weights)[1] 

# frontier_x is an array of values of Volatility
frontier_x = []

# determing Volatility for Returns
for ret in frontier_y:
    # the second constraint determines whether the Return obtained is the max possible Return
    constraints = ({'type':'eq','fun':check_sum}, {'type':'eq','fun': lambda w: ret_vol_sr(w)[0] - ret})
    
    result = minimize(min_vol, initial_guess, method='SLSQP', bounds=bounds, constraints=constraints)
    
    frontier_x.append(result['fun'])
    # the results of the minimize function has the index 'fun' which contains the actual value returned by the minimize function

# plotting the data
plt.figure(figsize=(12,8))
plt.scatter(volatility_arr,return_arr,c=sharpe_ratio_arr,cmap='plasma')
plt.colorbar(label='Sharpe Ratio')
plt.xlabel('Volatility')
plt.ylabel('Return')

# Add Efficient Frontier Curve
plt.plot(frontier_x,frontier_y,'r--',linewidth=2)
