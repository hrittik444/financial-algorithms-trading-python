### this algorithm was written and run in the Quantopian IDE

## Pairs Trading Algorithm

import numpy as np

def initialize(context):
    context.aal = sid(45971)
    context.ual = sid(28051)
    
    context.long_on_spread = False
    context.short_on_spread = False
    
    schedule_function(check_pairs, date_rules.every_day(), time_rules.market_close(minutes=60))
    
def check_pairs(context, data):
    
    aal = context.aal
    ual = context.ual
    
    prices = data.history([aal,ual], 'price', 30, '1d')
    print(prices)
    
    # the prices of AAL and UAL at the current time in the backtest
    short_prices = prices.iloc[-1:]
    
    # wrt the spread curve
    # moving avg and std deviation
    mavg_30 = np.mean(prices[aal] - prices[ual])
    std_30 = np.std(prices[aal] - prices[ual])
    
    # 1-day moving avg
    # ie: the current price of the spread
    mavg_1 = np.mean(short_prices[aal] - short_prices[ual])
    
    # calculating the z-score
    if std_30 > 0:
    # since we are working with 30-day rolling z-score
    
        zscore = (mavg_1-mavg_30) / std_30
        
        # entry cases:
        if zscore>0.5 and not context.short_on_spread:
           # remember spread = AAL - UAL price
           # if spread curve is above 0.5, that means AAL is currently over-valued and will eventually drop down
           # so go short on AAL and go long on UAL
           order_target_percent(aal,-0.5)
           order_target_percent(ual,0.5)
           context.short_on_spread = True
           context.long_on_spread = False
           
        elif zscore<0.5 and not context.long_on_spread:
           # if spread curve is below 0.5, that means UAL is currently over-valued and will eventually drop down
           # so go short on UAL and go long on AAL
           order_target_percent(ual,-0.5)
           order_target_percent(aal,0.5)
           context.short_on_spread = False
           context.long_on_spread = True
             
        # exit case     
        elif abs(zscore)<0.1:
           # when z-score is almost close to zero, liquidate and exit position     
           order_target_percent(ual,0)
           order_target_percent(aal,0)
           context.short_on_spread = False
           context.long_on_spread = False
             
        record(z_score_record = zscore)