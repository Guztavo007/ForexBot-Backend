
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from trading_logic import trade
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

selected_strategy = "sma_rsi"
selected_risk_level = 3

@app.post("/run")
async def run_bot(request: Request):
    body = await request.json()
    symbol = body.get("symbol", "EURUSD")
    alerts = body.get("alerts", {"enabled": False})

    # Dummy candle data - replace with live OANDA candle fetch if needed
    dummy_data = {
        "close": [1.101, 1.102, 1.105, 1.107, 1.106, 1.103, 1.101, 1.099, 1.100,
                  1.102, 1.105, 1.108, 1.107, 1.104, 1.102, 1.100, 1.098, 1.099, 1.097, 1.096],
        "high": [1.102, 1.103, 1.106, 1.108, 1.107, 1.104, 1.102, 1.100, 1.101,
                 1.103, 1.106, 1.109, 1.108, 1.105, 1.103, 1.101, 1.099, 1.100, 1.098, 1.097],
        "low": [1.100, 1.101, 1.104, 1.106, 1.105, 1.102, 1.100, 1.098, 1.099,
                1.101, 1.104, 1.107, 1.106, 1.103, 1.101, 1.099, 1.097, 1.098, 1.096, 1.095],
    }

    result = trade(dummy_data, strategy=selected_strategy, risk_level=selected_risk_level)

    # You can include alerts handling here if needed
    return JSONResponse(content={"trade": result})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
