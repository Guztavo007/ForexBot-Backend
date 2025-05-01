from fastapi import FastAPI
from strategy import run_strategy
from db import init_db, get_all_trades
from models import Trade
from fastapi.middleware.cors import CORSMiddleware
from daily_summary import get_daily_summary
from datetime import datetime, timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

@app.post("/run")
def run_bot():
    trade = run_strategy()
    return {"status": "executed", "trade": trade}

@app.get("/trades", response_model=list[Trade])
def get_trades():
    return get_all_trades()

@app.get("/summary")
def summary():
    since = datetime.utcnow() - timedelta(days=1)
    return get_daily_summary(since)