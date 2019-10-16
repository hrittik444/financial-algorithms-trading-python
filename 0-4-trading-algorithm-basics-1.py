### this algorithm was written and run in the Quantopian IDE

## test algorithm 1

# we shall consider our sample portfolio (Apple, Cisco, IBM, Amazon) at the optimized portfolio allocation that we calculated earlier

# the initialize function is called exactly once when the algorithm starts
# it takes context as args
# context is an augmented python dictionary that is used for maintaining the states of the algorithm during backtests or live trading
# context can be given properties and can be referenced in other parts of the algorithm
def initialize(context):
    # assigning Securities IDs for our stocks to context
    context.aapl = sid(24)
    context.csco = sid(1900)
    context.amzn = sid(16841)

# the handle_data function is called once at the end of each minute
# it takes context and data as args
# data stores several API functions
def handle_data(context, data):
    # order_target_percent places an order to adjust our position wrt our asset(s) to a specified percentage
    # upon performing portfolio optimization earlier, we had already calculated the optimal allocation for the various stocks in our portfolio
    order_target_percent(context.aapl,.27)
    order_target_percent(context.csco,.20)
    order_target_percent(context.amzn,.53)
    
    # so every minute, we are trying to rebalance oout portfolio to the optimal allocation specified, and sell/buy as needed