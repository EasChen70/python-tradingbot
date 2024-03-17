import ccxt 
from config import API_KEY, SECRET_KEY

exchange = ccxt.binanceus({
    'enableRateLimit': True,
    'apiKey': API_KEY,
    'secret': SECRET_KEY
})

balance = exchange.fetch_balance()

for currency, amount in balance['total'].items():
    if amount >= 0:
        print(f"{currency}: {amount}")