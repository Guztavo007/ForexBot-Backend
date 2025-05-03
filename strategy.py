from logger import log_decision
from datetime import datetime
import random

def get_current_price(symbol):
    return round(random.uniform(1.0900, 1.1000), 5)

def calculate_indicators(symbol):
    # Simulated indicator values
    return {
        "rsi": round(random.uniform(40, 60), 2),
        "sma": round(random.uniform(1.0900, 1.1000), 5)
    }

def run_strategy(symbol, alert_settings=None):
    price = get_current_price(symbol)
    indicators = calculate_indicators(symbol)

    # Simple mock strategy decision
    if indicators["rsi"] > 55:
        decision = "BUY"
    elif indicators["rsi"] < 45:
        decision = "SELL"
    else:
        decision = "HOLD"

    executed = decision in ["BUY", "SELL"]

    log_decision(
        symbol=symbol,
        strategy="sma_rsi",
        decision=decision,
        price=price,
        indicators=indicators,
        executed=executed
    )

    return {
        "symbol": symbol,
        "action": decision,
        "price": price,
        "indicators": indicators,
        "strategy": "sma_rsi"
    }
