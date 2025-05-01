import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1367633654087684118/fBKIgzAcYf11CnHcLvsPwXJfCADZKHwk9S5rx8em02bAI94cQsncwbobhgLeA2NACh9t"

def send_discord_alert(message):
    data = {"content": message}
    try:
        requests.post(WEBHOOK_URL, json=data)
    except Exception as e:
        print("Discord alert failed:", e)

def send_error_alert(error):
    message = f"⚠️ **Forex Bot Error**: {error}"
    send_discord_alert(message)