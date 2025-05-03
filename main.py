
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from trade_executor import execute_trade

app = FastAPI()

@app.post("/run")
async def run_bot(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(status_code=400, content={"error": "Invalid or missing JSON body."})

    symbol = body.get("symbol", "EUR_USD")
    alerts = body.get("alerts", {})
    result = execute_trade(symbol, alerts)
    return {"result": result}
