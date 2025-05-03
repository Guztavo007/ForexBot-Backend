
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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
        print("Received payload:", body)  # Debug print
        symbol = body.get("symbol")
        alerts = body.get("alerts", {})
        return {"status": "received", "symbol": symbol, "alerts": alerts}
    except Exception as e:
        print("Error in /run:", str(e))
        return {"error": str(e)}
