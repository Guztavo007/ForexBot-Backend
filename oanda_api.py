import requests
from config import OANDA_API_KEY, OANDA_ACCOUNT_ID, OANDA_URL

HEADERS = {
    "Authorization": f"Bearer {OANDA_API_KEY}",
    "Content-Type": "application/json"
}

def get_price(symbol):
    url = f"{OANDA_URL}/v3/accounts/{OANDA_ACCOUNT_ID}/pricing?instruments={symbol}"
    r = requests.get(url, headers=HEADERS)
    prices = r.json()["prices"][0]
    return float(prices["bids"][0]["price"])

def get_candles(symbol, count=30, granularity="M5"):
    url = f"{OANDA_URL}/v3/instruments/{symbol}/candles"
    params = {"count": count, "granularity": granularity, "price": "M"}
    r = requests.get(url, headers=HEADERS, params=params)
    return r.json()["candles"]

def place_order(symbol, side, units):
    data = {
        "order": {
            "instrument": symbol,
            "units": str(units if side == "buy" else -units),
            "type": "MARKET",
            "positionFill": "DEFAULT"
        }
    }
    url = f"{OANDA_URL}/v3/accounts/{OANDA_ACCOUNT_ID}/orders"
    r = requests.post(url, headers=HEADERS, json=data)
    return r.json()