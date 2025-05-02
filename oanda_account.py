import requests
import os

OANDA_API_KEY = os.getenv("OANDA_API_KEY", "bf7bd2751bc1e0d2ac56d60c24b36e27-9bf0f9a01f841ac5bb2c554be6f66ea8")
ACCOUNT_ID = os.getenv("OANDA_ACCOUNT_ID", "101-001-31619527-001")
BASE_URL = "https://api-fxpractice.oanda.com/v3"

def get_account_summary():
    url = f"{BASE_URL}/accounts/{ACCOUNT_ID}/summary"
    headers = {
        "Authorization": f"Bearer {OANDA_API_KEY}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()["account"]
        return {
            "balance": data["balance"],
            "equity": data["NAV"],
            "marginUsed": data["marginUsed"],
            "unrealizedPL": data["unrealizedPL"]
        }
    else:
        return {"error": response.json()}
