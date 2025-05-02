import requests
import os

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_alert(trade):
    if not DISCORD_WEBHOOK_URL:
        return

    message = f"**{trade['action']} {trade['symbol']}** at {trade.get('price', 'market')}"

    payload = {"content": message}
    headers = {"Content-Type": "application/json"}

    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload, headers=headers)
    except Exception as e:
        print("Failed to send Discord alert:", e)