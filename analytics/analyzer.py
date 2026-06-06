import pandas as pd
import numpy as np
from typing import List
from models import CryptoPrice

def calculate_analytics(prices: List[CryptoPrice]) -> List[dict]:
    analytics = []

    for price in prices:
        analytics.append({
            "symbol": price.symbol,
            "name": price.name,
            "current_price": price.price,
            "volume": price.volume,
            "market_cap": price.market_cap,
            "price_change_24h": price.price_change_24h,
            "signal_strength": "Strong" if abs(price.price_change_24h) > 5 else "Weak",
            "volume_rank": round(price.volume / 1_000_000, 2)
        })

    # Use pandas for ranking
    df = pd.DataFrame(analytics)
    df["market_rank"] = df["market_cap"].rank(ascending=False).astype(int)

    return df.to_dict(orient="records")