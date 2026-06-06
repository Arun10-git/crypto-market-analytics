from fastapi import FastAPI
from database import engine, Base
from routes.markets import router
from apscheduler.schedulers.background import BackgroundScheduler
from database import SessionLocal
from models import CryptoPrice
from fastapi.middleware.cors import CORSMiddleware
import requests

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Crypto Market Analytics",
    description="Real-time crypto market data and analytics API",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"

def scheduled_fetch():
    db = SessionLocal()
    try:
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 10,
            "page": 1
        }
        response = requests.get(COINGECKO_URL, params=params)
        data = response.json()
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
        print("Scheduled fetch completed!")
    finally:
        db.close()

scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_fetch, "interval", minutes=5)
scheduler.start()

@app.get("/")
def root():
    return {
        "message": "Crypto Market Analytics API",
        "docs": "/docs",
        "endpoints": [
            "/fetch",
            "/markets",
            "/prices?symbol=BTC",
            "/history?symbol=BTC",
            "/analytics",
            "/strategy/run"
        ]
    }