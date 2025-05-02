import requests
import datetime

def macd_strategy(symbol):
    url = f"https://api-fxpractice.oanda.com/v3/instruments/{symbol}/candles"
    headers = {
        "Authorization": "Bearer bf7bd2751bc1e0d2ac56d60c24b36e27-9bf0f9a01f841ac5bb2c554be6f66ea8"
    }
    params = {
        "granularity": "H1",
        "count": 100,
        "price": "M"
    }
    response = requests.get(url, headers=headers, params=params)
    candles = response.json().get("candles", [])

    closes = [float(c["mid"]["c"]) for c in candles if c["complete"]]

    def ema(data, span):
        alpha = 2 / (span + 1)
        ema_vals = [data[0]]
        for price in data[1:]:
            ema_vals.append((price - ema_vals[-1]) * alpha + ema_vals[-1])
        return ema_vals

    if len(closes) < 35:
        return {"symbol": symbol, "action": "hold", "price": closes[-1], "timestamp": datetime.datetime.utcnow().isoformat() + "Z"}

    macd_line = [a - b for a, b in zip(ema(closes, 12), ema(closes, 26))][-9:]
    signal_line = ema(macd_line, 9)

    latest_macd = macd_line[-1]
    latest_signal = signal_line[-1]

    if latest_macd > latest_signal:
        action = "buy"
    elif latest_macd < latest_signal:
        action = "sell"
    else:
        action = "hold"

    return {
        "symbol": symbol,
        "action": action,
        "price": closes[-1],
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }