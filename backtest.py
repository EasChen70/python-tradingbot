import ccxt 
import pandas as pd
import matplotlib.pyplot as plt
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
    
    #Make timestamp more readable
    dataset['timestamp'] = pd.to_datetime(dataset['timestamp'], unit='ms')
    #Calculate simple moving averages
    dataset['sma10'] = dataset.close.rolling(10).mean() #fast MA
    dataset['sma40'] = dataset.close.rolling(40).mean() #slow MA
    return dataset

# Make signals to buy/sell
def calc_signals(dataset):
    dataset['signal'] = 0
    dataset.loc[dataset['sma10'] > dataset['sma40'], 'signal'] = 1 #buy signal
    dataset.loc[dataset['sma10'] < dataset['sma40'], 'signal'] = -1 #sell signal
    dataset['signal'] = dataset['signal'].shift(1)
    return dataset

#Initialize functions
dataset = fetch_market('BTC/USDT', '1d', 90)
calc_signals(dataset)

#Backtest mock variables
initial_capital = 100
port_size = 1
current_position = None

trades = []

for index, row in dataset.iterrows():
    if row['signal'] == 1 and current_position is None:
        entry_price = row['close']
        trade_capital = initial_capital * port_size
        trade_quantity = trade_capital/entry_price
        current_position = 'buy'
        trades.append(('buy', row['timestamp'], entry_price, trade_quantity))
        print(f"Bought at {entry_price} on {row['timestamp'].date()}")
    elif row['signal'] == -1 and current_position == 'buy':
        exit_price = row['close']
        trade_capital = trade_quantity * exit_price
        initial_capital += trade_capital - (initial_capital * port_size)
        current_position = None
        trades.append(('sell', row['timestamp'], exit_price, trade_quantity))
        print(f"Sold at {exit_price} on {row['timestamp'].date()}")

trades_df = pd.DataFrame(trades, columns=['Action', 'Date', 'Price', 'Quantity'])
