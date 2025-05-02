import requests
import os

OANDA_API_URL = "https://api-fxpractice.oanda.com/v3"
ACCESS_TOKEN = os.getenv("OANDA_API_KEY")
ACCOUNT_ID = os.getenv("OANDA_ACCOUNT_ID")

def get_summary():
    url = f"{OANDA_API_URL}/accounts/{ACCOUNT_ID}/summary"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"error": response.text}

    data = response.json()["account"]
    return {
        "balance": float(data["balance"]),
        "equity": float(data["NAV"]),
        "marginUsed": float(data["marginUsed"]),
        "marginRate": float(data["marginRate"])
    }