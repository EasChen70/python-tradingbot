import ccxt 
import pandas as pd
from datetime import datetime, timedelta
from config import API_KEY, SECRET_KEY

exchange = ccxt.binanceus({
    'enableRateLimit': True,
    'apiKey': API_KEY,
    'secret': SECRET_KEY
})


# Moving Average Algo Strategy
def fetch_market(symbol, timeframe, limit):
    #Calculate historical data, for 'limit' days ago
    since = exchange.parse8601((datetime.now() - timedelta(days = limit)).isoformat())
    #Data starting from 'since'
    bars = exchange.fetch_ohlcv(symbol, timeframe, since)    
    dataset = pd.DataFrame(bars, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    
    #Make timstamp more readable
    dataset['timestamp'] = pd.to_datetime(dataset['timestamp'], unit='ms')
    #Calculate simple moving averages
    dataset['sma10'] = dataset.close.rolling(10).mean() #fast MA
    dataset['sma40'] = dataset.close.rolling(40).mean() #slow MA
    print(dataset)


fetch_market('BTC/USDT', '1d', 90)

## Swing Trading, buy = fast MA crosses above slow MA, sell = fast MA crosses above slow MA



# Fetches balance

# balance = exchange.fetch_balance()

# for currency, amount in balance['total'].items():
#     if amount >= 0:
#         print(f"{currency}: {amount}")


# Getting coin we want to trade

# symbol = 'BTC/USDT'

# ticker = exchange.fetch_ticker(symbol)

# print(ticker)
