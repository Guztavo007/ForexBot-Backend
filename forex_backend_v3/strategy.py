from oanda_api import get_price, get_candles, place_order
from db import log_trade
from discord_alerts import send_discord_alert, send_error_alert
import numpy as np

SYMBOL = "EUR_USD"
TRADE_UNITS = 100
RSI_PERIOD = 14
SMA_SHORT = 5
SMA_LONG = 20

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
        candles = get_candles(SYMBOL, count=max(SMA_LONG, RSI_PERIOD) + 1)
        closes = [float(c["mid"]["c"]) for c in candles]

        sma_short = calculate_sma(closes, SMA_SHORT)
        sma_long = calculate_sma(closes, SMA_LONG)
        rsi = calculate_rsi(closes, RSI_PERIOD)

        if sma_short is None or sma_long is None or rsi is None:
            return {"status": "Not enough data"}

        price = closes[-1]
        action = "hold"

        if sma_short > sma_long and rsi < 30:
            action = "buy"
        elif sma_short < sma_long and rsi > 70:
            action = "sell"

        if action != "hold":
            order = place_order(SYMBOL, action, TRADE_UNITS)
            trade = log_trade(SYMBOL, action, price)
            send_discord_alert(f"Trade Executed: {action.upper()} {SYMBOL} at {price:.5f}\nRSI: {rsi:.2f}, SMA Short: {sma_short:.5f}, SMA Long: {sma_long:.5f}")
            return trade

        return {"symbol": SYMBOL, "action": action, "price": price, "rsi": rsi, "sma_short": sma_short, "sma_long": sma_long}
    
    except Exception as e:
        send_error_alert(str(e))
        return {"status": "error", "detail": str(e)}