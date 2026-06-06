from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CryptoPriceSchema(BaseModel):
    id: int
    symbol: str
    name: str
    price: float
    volume: float
    market_cap: float
    price_change_24h: float
    timestamp: datetime

    class Config:
        from_attributes = True

class StrategyResult(BaseModel):
    symbol: str
    signal: str  # BUY / SELL / HOLD
    reason: str
    price: float