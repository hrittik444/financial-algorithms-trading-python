### this algorithm was written and run in the Quantopian IDE

## test algorithm 4

def initialize(context):
    context.amzn = sid(16841)
    context.ibm = sid(3766)
    
    schedule_function(rebalance, date_rules.every_day(), time_rules.market_open())
    schedule_function(record_variables, date_rules.every_day(), time_rules.market_close())
    
def rebalance(context, data):
    # going long on Amazon and short on IBM
    order_target_percent(context.amzn, 0.5)
    order_target_percent(context.ibm, -0.5)
    
def record_variables(context, data):
    # record allows us to record our algorithm against some additional data during the backtest (instead of just against the benchmark) 
    # so here, we are plotting the Adjusted Close prices of Amazon and IBM against our algorithm in the backtest plot
    record(amzn_close_record=data.current(context.amzn,'close'))
    record(ibm_close_record=data.current(context.ibm,'close'))