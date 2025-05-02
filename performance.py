import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def get_performance():
    trade_path = Path("trades.json")
    if not trade_path.exists():
        return {
            "total_trades": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0.0,
            "net_profit": 0.0,
            "average_pl": 0.0,
            "performance_over_time": []
        }

    with open(trade_path) as f:
        trades = json.load(f)

    wins = losses = total = 0
    net_profit = 0.0
    pl_by_day = defaultdict(float)

    for trade in trades:
        pl = float(trade.get("pl", 0))
        timestamp = trade.get("timestamp", "")
        date_key = timestamp.split("T")[0] if "T" in timestamp else "unknown"
        pl_by_day[date_key] += pl
        net_profit += pl
        total += 1
        if pl > 0:
            wins += 1
        elif pl < 0:
            losses += 1

    average_pl = net_profit / total if total > 0 else 0.0
    win_rate = wins / total if total > 0 else 0.0

    performance_over_time = [
        {"date": date, "pl": round(pl, 2)}
        for date, pl in sorted(pl_by_day.items())
    ]

    return {
        "total_trades": total,
        "wins": wins,
        "losses": losses,
        "win_rate": round(win_rate, 2),
        "net_profit": round(net_profit, 2),
        "average_pl": round(average_pl, 2),
        "performance_over_time": performance_over_time
    }