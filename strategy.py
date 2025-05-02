from oanda_api import get_price, get_candles, place_order
from db import log_trade
from discord_alerts import send_discord_alert, send_error_alert
from settings import load_settings
import numpy as np
import json
from datetime import datetime

LOG_FILE = "logs.json"

def log_decision(symbol, action, reason=""):
    log_entry = {
        "symbol": symbol,
        "action": action,
        "reason": reason,
        "timestamp": datetime.utcnow().isoformat()
    }
    try:
        logs = []
        try:
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        except:
            pass
        logs.append(log_entry)
        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=2)
    except Exception as e:
        print("Failed to log decision:", e)

def calculate_sma(values, period):
    return np.mean(values[-period:]) if len(values) >= period else None

def calculate_rsi(values, period=14):
    if len(values) < period + 1:
        return None
    deltas = np.diff(values)
    ups = deltas[deltas > 0].sum() / period
    downs = -deltas[deltas < 0].sum() / period
    rs = ups / downs if downs != 0 else 0
    return 100 - (100 / (1 + rs))

def run_strategy(symbol="EUR_USD"):
    try:
        settings = load_settings()
        strategy = settings.get("strategy", "sma_rsi")
        risk_level = int(settings.get("risk_level", 3))
        trade_units = 50 * risk_level

        candles = get_candles(symbol, count=30)
        closes = [float(c["mid"]["c"]) for c in candles]

        sma_short = calculate_sma(closes, 5)
        sma_long = calculate_sma(closes, 20)
        rsi = calculate_rsi(closes, 14)
        price = closes[-1]
        action = "hold"
        reason = ""

        if strategy == "sma_rsi":
            if sma_short > sma_long and rsi < 30:
                action = "buy"
                reason = "SMA crossover and RSI oversold"
            elif sma_short < sma_long and rsi > 70:
                action = "sell"
                reason = "SMA crossover and RSI overbought"
        elif strategy == "rsi_only":
            if rsi < 30:
                action = "buy"
                reason = "RSI oversold"
            elif rsi > 70:
                action = "sell"
                reason = "RSI overbought"
        elif strategy == "sma_only":
            if sma_short > sma_long:
                action = "buy"
                reason = "SMA crossover"
            elif sma_short < sma_long:
                action = "sell"
                reason = "SMA crossover"

        if action != "hold":
            place_order(symbol, action, trade_units)
            trade = log_trade(symbol, action, price)
            send_discord_alert(f"Trade: {action.upper()} {symbol} at {price:.5f}\n{reason}")
        else:
            log_decision(symbol, action, reason or "No trade conditions met")
            trade = {"symbol": symbol, "action": action, "price": price}

        return trade

    except Exception as e:
        send_error_alert(f"Error running strategy for {symbol}: {str(e)}")
        log_decision(symbol, "error", str(e))
        return {"status": "error", "detail": str(e)}
