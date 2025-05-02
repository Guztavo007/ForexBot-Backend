from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from strategy import run_strategy
from db import init_db, get_all_trades
from models import Trade
from settings import load_settings, save_settings

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

@app.get("/settings")
def get_settings():
    return load_settings()

@app.post("/settings")
async def update_settings(request: Request):
    body = await request.json()
    save_settings(body)
    return {"message": "Settings updated"}
