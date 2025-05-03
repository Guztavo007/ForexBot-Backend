import logging
import json
from datetime import datetime

logger = logging.getLogger("forex_bot")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("bot.log")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

def log_decision(symbol, strategy, decision, price, indicators, executed):
    log_entry = {
        "symbol": symbol,
        "strategy": strategy,
        "decision": decision,
        "price": price,
        "indicators": indicators,
        "executed": executed,
        "timestamp": datetime.utcnow().isoformat()
    }
    logger.info(json.dumps(log_entry))
