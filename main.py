
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/run")
async def run_bot(request: Request):
    try:
        body = await request.json()
        symbol = body.get("symbol", "EUR_USD")
        alerts = body.get("alerts", {})
        print(f"Executing bot for {symbol} with alerts: {alerts}")
        return {"status": "success", "action": "hold"}
    except Exception as e:
        print(f"Error in /run: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/logs")
def get_logs():
    return {"logs": ["Bot started", "Decision: HOLD", "No action taken"]}
