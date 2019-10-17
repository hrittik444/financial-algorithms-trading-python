### this algorithm was written and run in the Quantopian Research Notebook Environment

## some functions to demonstrate pipelines and related concepts - factors, filters, screens, masks and classifiers

## basic pipeline
from quantopian.pipeline import Pipeline
from quantopian.research import run_pipeline

# function that returns a pipeline
def new_pipeline():
    return Pipeline()

# runnning the pipeline function
results = run_pipeline(new_pipeline(), '2019-01-01', '2019-01-1')
print(result.head(10))


## pipeline with factors
# factors take in an asset and a timestamp and return some numerical value
# USEquityPricing contains pricing info on all the equities that we got above
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.factors import BollingerBands,SimpleMovingAverage,EWMA

def new_pipeline():
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=30)
    
    return Pipeline(columns={'30-Day Mean Close Price':mean_close_30})

results = run_pipeline(new_pipeline(), '2019-01-01', '2019-01-01')
print(results.head(10))

def new_pipeline():
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=30)
    latest_close = USEquityPricing.close.latest
    
    return Pipeline(columns={'30-Day Mean Close Price':mean_close_30, 'Latest Close Price':latest_close})

results = run_pipeline(new_pipeline(), '2019-01-01', '2019-01-01')
print(results.head(10))


## pipeline with a combination of factors
def new_pipeline():
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=30)
    mean_close_10 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=10)
    latest_close = USEquityPricing.close.latest
    
    percent_difference = (mean_close_10-mean_close_30)/mean_close_30
    
    return Pipeline(columns={'30-Day Mean Close Price':mean_close_30, 'Latest Close Price':latest_close, 'Percent Difference':percent_difference})

results = run_pipeline(new_pipeline(),'2017-01-01','2017-01-01')
print(results.head(10))


## pipeline with filter
# filters take in an asset and a timestamp and return a boolean
def new_pipeline():
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=30)
    mean_close_10 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=10)
    latest_close = USEquityPricing.close.latest
    
    percent_difference = (mean_close_10 - mean_close_30) / mean_close_30
    
    percent_difference_filter = percent_difference > 0
    
    return Pipeline(columns={'30-Day Mean Close Price':mean_close_30, 'Latest Close Price':latest_close, 'Percent Difference':percent_difference, 'Positive Percentage Difference Filter':percent_difference_filter})

results = run_pipeline(new_pipeline(),'2017-01-01','2017-01-01')

print(results.head(10))


## pipeline with filter and screen
def new_pipeline():
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=30)
    mean_close_10 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=10)
    latest_close = USEquityPricing.close.latest
    
    percent_difference = (mean_close_10 - mean_close_30) / mean_close_30
    
    percent_difference_filter = percent_difference > 0
    
    return Pipeline(columns={'30-Day Mean Close Price':mean_close_30, 'Latest Close Price':latest_close, 'Percent Difference':percent_difference, 'Positive Percentage Difference Filter':percent_difference_filter,}, 
                   screen=percent_difference_filter)

results = run_pipeline(new_pipeline(),'2017-01-01','2017-01-01')
print(results.head(10))


## pipeline with filter and reverse screen
def new_pipeline():
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=30)
    mean_close_10 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=10)
    latest_close = USEquityPricing.close.latest
    
    percent_difference = (mean_close_10 - mean_close_30) / mean_close_30
    
    percent_difference_filter = percent_difference > 0
    
    return Pipeline(columns={'30-Day Mean Close Price':mean_close_30, 'Latest Close Price':latest_close, 'Percent Difference':percent_difference, 'Positive Percentage Difference Filter':percent_difference_filter,}, 
                   screen=~percent_difference_filter)

results = run_pipeline(new_pipeline(),'2017-01-01','2017-01-01')
print(results.head(10))


## pipeline with a combination of filters
def new_pipeline():
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=30)
    mean_close_10 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=10)
    latest_close = USEquityPricing.close.latest
    
    percent_difference = (mean_close_10 - mean_close_30) / mean_close_30
    
    percent_difference_filter = percent_difference > 0
    small_price_stocks_filter = latest_close < 5
    
    combined_filter = percent_difference_filter & small_price_stocks_filter
    
    return Pipeline(columns={'30-Day Mean Close Price':mean_close_30, 'Latest Close Price':latest_close, 'Percent Difference':percent_difference, 'Positive Percentage Difference Filter':percent_difference_filter,}, 
                   screen=combined_filter)

results = run_pipeline(new_pipeline(),'2017-01-01','2017-01-01')
print(results.head(10))


## pipeline with masks
# masks allow us to ignore certain assets when computing pipeline expresssions
def new_pipeline():
    latest_close = USEquityPricing.close.latest
    small_price_stocks = latest_close < 5
    
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=30, mask=small_price_stocks)
    mean_close_10 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=10, mask=small_price_stocks)
    
    
    percent_difference = (mean_close_10 - mean_close_30) / mean_close_30
    percent_difference_filter = percent_difference > 0
    combined_filter = percent_difference_filter
    
    return Pipeline(columns={'30-Day Mean Close Price':mean_close_30, 'Latest Close Price':latest_close, 'Percent Difference':percent_difference, 'Positive Percentage Difference Filter':percent_difference_filter,}, 
                   screen=combined_filter)

results = run_pipeline(new_pipeline(),'2017-01-01','2017-01-01')
print(results.head(10))
print(len(results))


## pipeline with classifier
# classifiers take in an asset and a timestamp and return a categorical output such as a string or integer label
# here we are using the morningstar's Sector classifier
from quantopian.pipeline.data import morningstar
from quantopian.pipeline.classifiers.morningstar import Sector

morningstar_sector = Sector()
exchange = morningstar.share_class_reference.exchange_id.latest
print(exchange)

# common classifier methods:
    # eq (equals)
    # isnull
    # startswith

def new_pipeline():
    latest_close = USEquityPricing.close.latest
    small_price_stocks = latest_close < 5
    
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=30, mask=small_price_stocks)
    mean_close_10 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=10, mask=small_price_stocks)
    
    # using a classifier to check filter only stocks that belong to the NYSE
    nyse_filter = exchange.eq('NYS')
    
    percent_difference = (mean_close_10 - mean_close_30) / mean_close_30
    percent_difference_filter = percent_difference > 0
    combined_filter = percent_difference_filter & nyse_filter
    
    return Pipeline(columns={'30-Day Mean Close Price':mean_close_30, 'Latest Close Price':latest_close, 'Percent Difference':percent_difference, 'Positive Percentage Difference Filter':percent_difference_filter,}, 
                   screen=combined_filter)

results = run_pipeline(new_pipeline(),'2017-01-01','2017-01-01')
print(results.head(10))
print(len(results))
