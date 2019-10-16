### this algorithm was written and run in the Quantopian IDE

## Bollinger Bands Trading Algorithm

# our simple strategy is as follows:
    # if at any point the stock's price goes above the Upper Bollinger Band, it would mean that the stock is overvalued and price will come down eventually
    # so we will go short
    # if at any point the stock's price goes below the Lower Bollinger Band, it would mean that the stock is undervalued and price will go up eventually
    # so we will go long
    
def initialize(context):
    context.tsla = sid(39840)
    
    schedule_function(check_bol, date_rules.every_day());
    
def check_bol(context, data):
    
    # getting current price
    current_price = data.current(context.tsla, 'price')
    
    # getting historic prices
    prices = data.history(context.tsla, 'price', 30, '1d')
    
    # getting avg and std deviation of historic prices
    avg_price = prices.mean()
    std_price = prices.std()
    
    # computing Upper and Lower Bollinger Bands
    upper_band = avg_price + 2*std_price
    lower_band = avg_price - 2*std_price
    
    # STRATEGY:
    if current_price >= upper_band:
        order_target_percent(context.tsla, -1.0)
        print('SHORTING TSLA')
        print("Current Price: {}".format(current_price))
        
    elif current_price <= lower_band:
        order_target_percent(context.tsla, 1.0)
        print('BUYING TSLA')
        print("Current Price: {}".format(current_price))
        
    else:
        pass
    
    record(Upper=upper_band, Lower=lower_band, Current=current_price, Average=avg_price)