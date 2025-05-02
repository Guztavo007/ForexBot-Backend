import requests

API_KEY = "bf7bd2751bc1e0d2ac56d60c24b36e27-9bf0f9a01f841ac5bb2c554be6f66ea8"
ACCOUNT_ID = "101-001-31619527-001"
API_URL = "https://api-fxpractice.oanda.com/v3"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def get_price(symbol):
    url = f"{API_URL}/accounts/{ACCOUNT_ID}/pricing?instruments={symbol}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    prices = r.json()
    return float(prices["prices"][0]["bids"][0]["price"])

def get_candles(symbol, count=30, granularity="M5"):
    url = f"{API_URL}/instruments/{symbol}/candles"
    params = {
        "count": count,
        "granularity": granularity,
        "price": "M"
    }
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    candles = r.json()["candles"]
    return [c for c in candles if c["complete"]]

def place_order(symbol, side, units):
    data = {
        "order": {
            "units": str(units if side == "buy" else -units),
            "instrument": symbol,
            "timeInForce": "FOK",
            "type": "MARKET",
            "positionFill": "DEFAULT"
        }
    }
    url = f"{API_URL}/accounts/{ACCOUNT_ID}/orders"
    r = requests.post(url, headers=HEADERS, json=data)
    r.raise_for_status()
    return r.json()
