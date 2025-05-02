from fastapi import FastAPI, Request
from strategy import run_strategy
from logger import log_decision
from discord_alerts import send_alert
import uvicorn

app = FastAPI()

@app.post("/run")
async def run_bot(request: Request):
    body = await request.json()
    symbol = body.get("symbol", "EUR_USD")
    alerts = body.get("alerts", {})
    try:
        trade = run_strategy(symbol)
        log_decision(trade)
        if alerts.get("enabled"):
            if trade["action"] in ["BUY", "SELL"] and alerts.get("trades"):
                send_alert(trade)
            elif trade["action"] == "HOLD" and alerts.get("holds"):
                send_alert(trade)
            elif trade["action"] == "ERROR" and alerts.get("errors"):
                send_alert(trade)
        return {"status": "success", "trade": trade}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
