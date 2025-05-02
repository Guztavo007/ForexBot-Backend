import requests
import os

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "https://discord.com/api/webhooks/your_webhook_here")

def send_alert(trade):
    content = f"**{trade['symbol']}**\nAction: **{trade['action']}**\nReason: {trade.get('reason', 'N/A')}\nIndicators: {trade.get('indicators', {})}"
    requests.post(WEBHOOK_URL, json={"content": content})
