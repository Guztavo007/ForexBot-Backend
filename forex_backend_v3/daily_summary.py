from db import get_all_trades
from discord_alerts import send_discord_alert
from datetime import datetime, timedelta

def get_daily_summary(since: datetime):
    trades = get_all_trades()
    summary_trades = [t for t in trades if datetime.fromisoformat(t['timestamp']) >= since]

    if not summary_trades:
        return {"summary": "No trades in the last 24 hours."}

    msg = f"📊 **Daily Trade Summary ({len(summary_trades)} trades)**\n"
    for t in summary_trades:
        msg += f"- {t['timestamp'][:16]} | {t['action'].upper()} {t['symbol']} at {t['price']:.5f}\n"

    send_discord_alert(msg)
    return {"summary": msg}