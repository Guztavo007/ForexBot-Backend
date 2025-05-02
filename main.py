from fastapi import FastAPI, Request
from strategy import run_strategy
from oanda_account import get_summary
from discord_alerts import send_alert
import json

app = FastAPI()

@app.post("/run")
async def run_bot(request: Request):
    body = await request.json()
    symbol = body.get("symbol", "EUR_USD")
    alerts = body.get("alerts", {})
    try:
        trade = run_strategy(symbol)
        if alerts.get("enabled") and alerts.get("trades") and trade["action"] in ("BUY", "SELL"):
            send_alert(f"{symbol} - Trade executed: {trade['action']} at {trade['price']}")
        elif alerts.get("enabled") and alerts.get("holds") and trade["action"] == "HOLD":
            send_alert(f"{symbol} - Bot decision: HOLD")
        return trade
    except Exception as e:
        if alerts.get("enabled") and alerts.get("errors"):
            send_alert(f"{symbol} - Error during trade decision: {str(e)}")
        return {"status": "error", "detail": str(e)}

@app.post("/settings")
async def save_settings(request: Request):
    data = await request.json()
    with open("settings.json", "w") as f:
        json.dump(data, f)
    return {"status": "saved"}

@app.get("/performance")
def performance():
    try:
        with open("trade_history.json") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []
    total = len(history)
    wins = [t for t in history if t.get("pl", 0) > 0]
    net_profit = sum(t.get("pl", 0) for t in history)
    avg_pl = (net_profit / total) if total else 0
    return {
        "total_trades": total,
        "win_rate": len(wins) / total if total else 0,
        "net_profit": net_profit,
        "average_pl": avg_pl,
        "performance_over_time": history[-30:]
    }

@app.get("/account-summary")
def account_summary():
    return get_summary()