from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import CryptoPrice
from analytics.analyzer import calculate_analytics
from strategy.signals import run_strategy
import requests

router = APIRouter()

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"

def fetch_crypto_data():
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1
    }
    response = requests.get(COINGECKO_URL, params=params)
    return response.json()

def get_latest_prices(db):
    seen = set()
    all_prices = db.query(CryptoPrice).order_by(
        CryptoPrice.timestamp.desc()
    ).all()
    prices = []
    for p in all_prices:
        if p.symbol not in seen:
            seen.add(p.symbol)
            prices.append(p)
    return prices

@router.post("/fetch")
def fetch_and_store(db: Session = Depends(get_db)):
    data = fetch_crypto_data()
    for coin in data:
        price = CryptoPrice(
            symbol=coin["symbol"].upper(),
            name=coin["name"],
            price=coin["current_price"],
            volume=coin["total_volume"],
            market_cap=coin["market_cap"],
            price_change_24h=coin["price_change_percentage_24h"]
        )
        db.add(price)
    db.commit()
    return {"message": "Data fetched and stored!", "count": len(data)}

@router.get("/markets")
def get_markets(db: Session = Depends(get_db)):
    return get_latest_prices(db)

@router.get("/prices")
def get_price(symbol: str, db: Session = Depends(get_db)):
    price = db.query(CryptoPrice).filter(
        CryptoPrice.symbol == symbol.upper()
    ).order_by(CryptoPrice.timestamp.desc()).first()
    return price

@router.get("/history")
def get_history(symbol: str, limit: int = 100, db: Session = Depends(get_db)):
    history = db.query(CryptoPrice).filter(
        CryptoPrice.symbol == symbol.upper()
    ).order_by(CryptoPrice.timestamp.desc()).limit(limit).all()
    return history

@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db)):
    prices = get_latest_prices(db)
    return calculate_analytics(prices)

@router.post("/strategy/run")
def run_strategy_endpoint(db: Session = Depends(get_db)):
    prices = get_latest_prices(db)
    return run_strategy(prices)