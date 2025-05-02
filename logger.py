from pathlib import Path
import json
from datetime import datetime

def log_decision(result):
    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "symbol": result.get("symbol"),
        "action": result.get("action"),
        "reason": result.get("reason", "")
    }

    path = Path("logs.json")
    logs = []
    if path.exists():
        with open(path) as f:
            logs = json.load(f)

    logs.append(log)
    with open(path, "w") as f:
        json.dump(logs, f, indent=2)