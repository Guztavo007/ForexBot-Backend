from logger import log_decision
from datetime import datetime

def run_strategy(symbol, alert_settings=None):
    decision = "BUY"
    price = 1.0950
    indicators = {
        "rsi": 58,
        "sma": 1.093
    }

    log_decision(
        symbol=symbol,
        strategy="sma_rsi",
        decision=decision,
        price=price,
        indicators=indicators,
        executed=True
    )

    return {
        "symbol": symbol,
        "action": decision,
        "price": price,
        "indicators": indicators,
        "strategy": "sma_rsi"
    }
