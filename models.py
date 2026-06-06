from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from datetime import datetime

class CryptoPrice(Base):
    __tablename__ = "crypto_prices"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    name = Column(String)
    price = Column(Float)
    volume = Column(Float)
    market_cap = Column(Float)
    price_change_24h = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)