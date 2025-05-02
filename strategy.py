from oanda_api import get_price, get_candles, place_order
from db import log_trade
from discord_alerts import send_discord_alert, send_error_alert
from settings import load_settings
import numpy as np

SYMBOL = "EUR_USD"

def calculate_sma(values, period):
    if len(values) < period:
        return None
    return np.mean(values[-period:])

def calculate_rsi(values, period=14):
    if len(values) < period + 1:
        return None
    deltas = np.diff(values)
    ups = deltas[deltas > 0].sum() / period
    downs = -deltas[deltas < 0].sum() / period
    rs = ups / downs if downs != 0 else 0
    return 100 - (100 / (1 + rs))

def run_strategy():
    try:
        settings = load_settings()
        strategy = settings.get("strategy", "sma_rsi")
        risk_level = int(settings.get("risk_level", 3))
        trade_units = 50 * risk_level

        candles = get_candles(SYMBOL, count=30)
        closes = [float(c["mid"]["c"]) for c in candles]

        sma_short = calculate_sma(closes, 5)
        sma_long = calculate_sma(closes, 20)
        rsi = calculate_rsi(closes, 14)
        price = closes[-1]
        action = "hold"

        if strategy == "sma_rsi":
            if sma_short > sma_long and rsi < 30:
                action = "buy"
            elif sma_short < sma_long and rsi > 70:
                action = "sell"
        elif strategy == "rsi_only":
            if rsi < 30:
                action = "buy"
            elif rsi > 70:
                action = "sell"
        elif strategy == "sma_only":
            if sma_short > sma_long:
                action = "buy"
            elif sma_short < sma_long:
                action = "sell"

        if action != "hold":
            order = place_order(SYMBOL, action, trade_units)
            trade = log_trade(SYMBOL, action, price)
            send_discord_alert(f"Trade Executed: {action.upper()} {SYMBOL} at {price:.5f}\nStrategy: {strategy}, RSI: {rsi:.2f}, SMA: {sma_short:.5f}/{sma_long:.5f}")
            return trade

        return {{"symbol": SYMBOL, "action": action, "price": price, "rsi": rsi, "sma_short": sma_short, "sma_long": sma_long}}

    except Exception as e:
        send_error_alert(str(e))
        return {{"status": "error", "detail": str(e)}}
