import datetime

def log_decision(trade):
    timestamp = datetime.datetime.utcnow().isoformat()
    with open("trade_logs.txt", "a") as f:
        f.write(f"[{timestamp}] {trade['symbol']} | Action: {trade['action']} | Reason: {trade.get('reason', 'N/A')} | Indicators: {trade.get('indicators', {})}\n")
