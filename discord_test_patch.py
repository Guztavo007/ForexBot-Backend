
from fastapi import APIRouter
import os
import requests

router = APIRouter()

@router.get("/test-discord")
async def test_discord():
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        return {"error": "Webhook URL not set"}

    message = {"content": "✅ Test alert: Webhook is working!"}
    r = requests.post(webhook_url, json=message)
    return {"status": r.status_code}
