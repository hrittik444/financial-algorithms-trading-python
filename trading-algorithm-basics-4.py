### this algorithm was written and run in the Quantopian IDE

## test algorithm 4

# scheduling functions
# putting functions in handle_data will execute every minute and we may not want that so we will need to schedule functions

def initialize(context):
    context.aapl = sid(24)
    
    # scheduling our functions
    schedule_function(open_positions, date_rules.week_start(), time_rules.market_open())
    schedule_function(close_positions, date_rules.week_end(), time_rules.market_close(minutes=30))
    
def open_positions(context, data):
    order_target_percent(context.aapl, 0.10)
    
def close_positions(context, data):
    order_target_percent(context.aapl,0)