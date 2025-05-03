
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with your frontend URL for more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/run")
async def run_bot(request: Request):
    body = await request.json()
    symbol = body.get("symbol", "EUR_USD")
    alerts = body.get("alerts", {})
    return {"status": "executed", "symbol": symbol, "alerts": alerts}

@app.get("/test-discord")
def test_discord():
    webhook_url = os.getenv("Discord_Webhook_URL")
    if not webhook_url:
        return {"error": "Webhook URL not set"}
    return {"status": "Webhook URL is set"}
