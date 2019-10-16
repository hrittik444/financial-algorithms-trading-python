### this algorithm was written and run in the Quantopian IDE

## test algorithm 2

def initialize(context):
    # creating a list of Securities IDs
    context.tech_stocks = [sid(24),sid(1900),sid(16841)]
    print(type(context.tech_stocks))

def handle_data(context, data):
    # getting the current adjusted closing price of our asset(s)
    tech_stocks_close = data.current(context.tech_stocks,'close')
    print(tech_stocks_close)
    print('\n')
    print(type(tech_stocks_close))
    
    # so every minute,, we are grabbing the closing price of tech stocks in our portfolio and printing it out as a Pandas series
    # we can use this to do stuff like, say if at the current minute, Apple stock is higher than Cisco, sell Apple and buy Cicso, etc.
    
    # checking if our data about our assets is up to date
    print(data.is_stale([sid(24),sid(1900),sid(16841)]))
    print('\n')
    
    # checking whether our asset(s) are alive and has trading
    if(data.can_trade(sid(24)) and data.can_trade(sid(1900)) and data.can_trade(sid(16841))):
        order_target_percent(sid(24),.27)
        order_target_percent(sid(1900),.20)
        order_target_percent(sid(16841),.53)