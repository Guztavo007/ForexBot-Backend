import requests
import statistics
import datetime

def bollinger_strategy(symbol):
    url = f"https://api-fxpractice.oanda.com/v3/instruments/{symbol}/candles"
    headers = {
        "Authorization": "Bearer bf7bd2751bc1e0d2ac56d60c24b36e27-9bf0f9a01f841ac5bb2c554be6f66ea8"
    }
    params = {
        "granularity": "H1",
        "count": 21,
        "price": "M"
    }
    response = requests.get(url, headers=headers, params=params)
    candles = response.json().get("candles", [])

    closes = [float(c["mid"]["c"]) for c in candles if c["complete"]]

    if len(closes) < 20:
        return {"symbol": symbol, "action": "hold", "price": closes[-1], "timestamp": datetime.datetime.utcnow().isoformat() + "Z"}

    sma = statistics.mean(closes[-20:])
    stddev = statistics.stdev(closes[-20:])
    upper = sma + (2 * stddev)
    lower = sma - (2 * stddev)
    price = closes[-1]

    if price <= lower:
        action = "buy"
    elif price >= upper:
        action = "sell"
    else:
        action = "hold"

    return {
        "symbol": symbol,
        "action": action,
        "price": price,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }