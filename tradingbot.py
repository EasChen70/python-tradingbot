import ccxt 
from config import API_KEY, SECRET_KEY

exchange = ccxt.coinbase({
    'apiKey': API_KEY,
    'secretKey': SECRET_KEY
})