from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from strategy import run_strategy
from logger import log_decision
from trade_executor import execute_trade
from settings import save_settings, load_settings
from performance import get_performance
import json
from pathlib import Path
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RunRequest(BaseModel):
    symbol: str

class SettingsRequest(BaseModel):
    risk_level: int
    strategy: str

@app.post("/run")
def run_bot(req: RunRequest):
    result = run_strategy(req.symbol)
    log_decision(result)
    executed_trade = execute_trade(result)
    return {"trade": executed_trade}

@app.post("/settings")
def update_settings(settings: SettingsRequest):
    save_settings(settings.dict())
    return {"status": "success"}

@app.get("/settings")
def get_settings():
    return load_settings()

@app.get("/trades")
def get_trades():
    path = Path("trades.json")
    if not path.exists():
        return []
    with open(path) as f:
        return json.load(f)

@app.get("/logs")
def get_logs():
    path = Path("logs.json")
    if not path.exists():
        return []
    with open(path) as f:
        return json.load(f)

@app.get("/account-summary")
def get_account_summary():
    from oanda_account import get_summary
    return get_summary()

@app.get("/performance")
def performance():
    return get_performance()
