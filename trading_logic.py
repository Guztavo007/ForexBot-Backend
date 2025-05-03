import numpy as np

def trade(data, strategy="sma_rsi", risk_level=3):
    try:
        if strategy == "sma_rsi":
            return sma_rsi_strategy(data, risk_level)
        elif strategy == "macd":
            return macd_strategy(data, risk_level)
        elif strategy == "bollinger":
            return bollinger_strategy(data, risk_level)
        elif strategy == "breakout":
            return breakout_strategy(data, risk_level)
        else:
            return {"action": "HOLD", "reason": "Invalid strategy"}
    except Exception as e:
        return {"action": "HOLD", "reason": f"Error in strategy: {str(e)}"}

def sma_rsi_strategy(data, risk_level):
    close_prices = np.array(data["close"])
    if len(close_prices) < 20:
        return {"action": "HOLD", "reason": "Not enough data"}

    sma_short = np.mean(close_prices[-5:])
    sma_long = np.mean(close_prices[-15:])
    delta = np.diff(close_prices)
    gain = np.mean([d for d in delta[-14:] if d > 0] or [0])
    loss = -np.mean([d for d in delta[-14:] if d < 0] or [0])
    rs = gain / loss if loss != 0 else float('inf')
    rsi = 100 - (100 / (1 + rs))

    if sma_short > sma_long and rsi < 70:
        return {"action": "BUY", "reason": f"SMA Crossover + RSI({rsi:.2f})"}
    elif sma_short < sma_long and rsi > 30:
        return {"action": "SELL", "reason": f"SMA Crossdown + RSI({rsi:.2f})"}
    else:
        return {"action": "HOLD", "reason": f"SMA and RSI neutral ({rsi:.2f})"}

def macd_strategy(data, risk_level):
    close = np.array(data["close"])
    if len(close) < 35:
        return {"action": "HOLD", "reason": "Not enough data for MACD"}

    ema12 = np.convolve(close[-35:], np.ones(12)/12, mode='valid')[-1]
    ema26 = np.convolve(close[-35:], np.ones(26)/26, mode='valid')[-1]
    macd = ema12 - ema26
    signal = np.convolve(close[-35:], np.ones(9)/9, mode='valid')[-1]

    if macd > signal:
        return {"action": "BUY", "reason": "MACD crossover"}
    elif macd < signal:
        return {"action": "SELL", "reason": "MACD crossdown"}
    else:
        return {"action": "HOLD", "reason": "MACD neutral"}

def bollinger_strategy(data, risk_level):
    close = np.array(data["close"])
    if len(close) < 20:
        return {"action": "HOLD", "reason": "Not enough data for Bollinger"}

    sma = np.mean(close[-20:])
    std = np.std(close[-20:])
    upper = sma + 2 * std
    lower = sma - 2 * std
    current = close[-1]

    if current > upper:
        return {"action": "SELL", "reason": "Price above upper band"}
    elif current < lower:
        return {"action": "BUY", "reason": "Price below lower band"}
    else:
        return {"action": "HOLD", "reason": "Price within bands"}

def breakout_strategy(data, risk_level):
    high = max(data["high"][-20:])
    low = min(data["low"][-20:])
    current = data["close"][-1]

    if current > high:
        return {"action": "BUY", "reason": "Breakout above resistance"}
    elif current < low:
        return {"action": "SELL", "reason": "Breakout below support"}
    else:
        return {"action": "HOLD", "reason": "No breakout"}