import requests
import datetime

def breakout_strategy(symbol):
    url = f"https://api-fxpractice.oanda.com/v3/instruments/{symbol}/candles"
    headers = {
        "Authorization": "Bearer bf7bd2751bc1e0d2ac56d60c24b36e27-9bf0f9a01f841ac5bb2c554be6f66ea8"
    }
    params = {
        "granularity": "H1",
        "count": 50,
        "price": "M"
    }
    response = requests.get(url, headers=headers, params=params)
    candles = response.json().get("candles", [])

    highs = [float(c["mid"]["h"]) for c in candles if c["complete"]]
    lows = [float(c["mid"]["l"]) for c in candles if c["complete"]]
    closes = [float(c["mid"]["c"]) for c in candles if c["complete"]]

    if len(closes) < 50:
        return {"symbol": symbol, "action": "hold", "price": closes[-1], "timestamp": datetime.datetime.utcnow().isoformat() + "Z"}

    resistance = max(highs[-20:])
    support = min(lows[-20:])
    price = closes[-1]

    if price > resistance:
        action = "buy"
    elif price < support:
        action = "sell"
    else:
        action = "hold"

    return {
        "symbol": symbol,
        "action": action,
        "price": price,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }