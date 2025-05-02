from hybrid_strategy import hybrid_sma_rsi
from macd_strategy import macd_strategy
from bollinger_strategy import bollinger_strategy
from breakout_strategy import breakout_strategy
from settings import load_settings

def run_strategy(symbol):
    settings = load_settings()
    strategy = settings.get("strategy", "sma_rsi")

    if strategy == "macd":
        return macd_strategy(symbol)
    elif strategy == "bollinger":
        return bollinger_strategy(symbol)
    elif strategy == "breakout":
        return breakout_strategy(symbol)
    else:
        return hybrid_sma_rsi(symbol)