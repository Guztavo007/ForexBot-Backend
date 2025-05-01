from pydantic import BaseModel

class Trade(BaseModel):
    symbol: str
    action: str
    price: float
    timestamp: str