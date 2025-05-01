import sqlite3
from datetime import datetime

DB_NAME = "trades.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT,
                action TEXT,
                price REAL,
                timestamp TEXT
            )
        """)

def log_trade(symbol, action, price):
    timestamp = datetime.utcnow().isoformat()
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "INSERT INTO trades (symbol, action, price, timestamp) VALUES (?, ?, ?, ?)",
            (symbol, action, price, timestamp)
        )
    return {"symbol": symbol, "action": action, "price": price, "timestamp": timestamp}

def get_all_trades():
    with sqlite3.connect(DB_NAME) as conn:
        rows = conn.execute("SELECT symbol, action, price, timestamp FROM trades").fetchall()
    return [{"symbol": r[0], "action": r[1], "price": r[2], "timestamp": r[3]} for r in rows]