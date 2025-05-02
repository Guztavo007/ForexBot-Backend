
from fastapi import APIRouter, Request
from strategy import run_strategy

router = APIRouter()

@router.post("/run")
async def run_bot(request: Request):
    try:
        body = await request.json()
    except Exception:
        body = {}

    symbol = body.get("symbol", "EUR_USD")
    alerts = body.get("alerts", {})
    result = run_strategy(symbol=symbol, alert_settings=alerts)
    return result
