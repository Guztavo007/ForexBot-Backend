from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from strategy import run_strategy
from settings import load_settings, save_settings
import json
from pathlib import Path
from datetime import datetime

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/run")
async def run_bot(request: Request):
    try:
        body = await request.json()
    except:
        body = {}
    symbol = body.get("symbol", "EUR_USD")
    trade = run_strategy(symbol)
    return {"status": "executed", "trade": trade}

@app.post("/settings")
async def update_settings(request: Request):
    data = await request.json()
    save_settings(data)
    return {"message": "Settings updated"}

@app.get("/settings")
def get_settings():
    return load_settings()

@app.get("/logs")
def get_logs(
    symbol: str = Query(None),
    action: str = Query(None),
    since: str = Query(None)
):
    log_path = Path("logs.json")
    if not log_path.exists():
        return []

    with open(log_path) as f:
        logs = json.load(f)

    if symbol:
        logs = [log for log in logs if log.get("symbol") == symbol]
    if action:
        logs = [log for log in logs if log.get("action") == action]
    if since:
        try:
            since_dt = datetime.fromisoformat(since.replace("Z", "+00:00"))
            logs = [log for log in logs if datetime.fromisoformat(log["timestamp"].replace("Z", "+00:00")) >= since_dt]
        except Exception as e:
            return {"error": f"Invalid 'since' format: {str(e)}"}

    return logs
