from fastapi import APIRouter
import json

router = APIRouter()

@router.get("/logs")
def get_logs():
    logs = []
    try:
        with open("bot.log") as f:
            for line in f:
                try:
                    logs.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        return {"logs": []}
    
    return {"logs": logs[-100:]}  # last 100 entries
