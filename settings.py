import json
from pathlib import Path

SETTINGS_FILE = Path("settings.json")

DEFAULT_SETTINGS = {
    "risk_level": 3,
    "strategy": "sma_rsi"
}

def load_settings():
    if SETTINGS_FILE.exists():
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_SETTINGS

def save_settings(new_settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(new_settings, f)
