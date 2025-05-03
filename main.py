from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from trading_logic import trade  # assuming your strategy logic is in trading_logic.py
from logger import log_decision  # assuming this is your custom logging module

app = FastAPI()

@app.post("/run")
async def run_bot(request: Request):
    try:
        body = await request.json()
        alerts = body.get("alerts", {})
        symbol = body.get("symbol", "EUR_USD")  # fallback to EUR_USD

        print(f"⚙️ Running bot for {symbol} with alerts: {alerts}")
        result = trade(symbol, alerts)
        print("📤 Trade result:", result)

        # Ensure logging is always called
        log_decision({
            "symbol": symbol,
            "action": result.get("action", "none"),
            "details": result
        })

        return JSONResponse(content={"status": "success", "trade": result})
    except Exception as e:
        print("🔥 Exception in /run:", str(e))
        return JSONResponse(content={"error": str(e)}, status_code=500)
