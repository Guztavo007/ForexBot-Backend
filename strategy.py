def run_strategy(symbol):
    # Simulated decision for demonstration
    return {
        "symbol": symbol,
        "action": "HOLD",
        "reason": "RSI is neutral, no clear SMA crossover",
        "indicators": {
            "RSI": 51.2,
            "SMA_50": 1.1234,
            "SMA_200": 1.1240
        }
    }
