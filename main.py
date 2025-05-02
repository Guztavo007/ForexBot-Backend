from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from strategy import run_strategy
from settings import load_settings, save_settings
import json
from pathlib import Path

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/run")
async def run_bot(request: Request):
    body = await request.json()
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
def get_logs():
    log_path = Path("logs.json")
    if log_path.exists():
        with open(log_path) as f:
            return json.load(f)
    return []
