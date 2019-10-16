### this algorithm was written and run in the Quantopian IDE

## test algorithm 3

def initialize(context):
    context.tech_stocks = [sid(24),sid(1900),sid(16841)]
    print(type(context.tech_stocks))

def handle_data(context, data):
  
    # viewing historical price data about our asset(s) for every 5 days
    # see: https://www.quantopian.com/docs/api-reference/algorithm-api-reference#id2
    tech_stocks_history = data.history(context.tech_stocks, fields='price', bar_count=5, frequency='1d')
    print(tech_stocks_history)