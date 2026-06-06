from typing import List
from models import CryptoPrice

def run_strategy(prices: List[CryptoPrice]) -> List[dict]:
    results = []

    for price in prices:
        change = price.price_change_24h

        if change > 5:
            signal = "BUY"
            reason = f"{price.symbol} is up {change:.2f}% — strong momentum"
        elif change < -5:
            signal = "SELL"
            reason = f"{price.symbol} is down {change:.2f}% — bearish trend"
        else:
            signal = "HOLD"
            reason = f"{price.symbol} is stable at {change:.2f}% change"

        results.append({
            "symbol": price.symbol,
            "name": price.name,
            "price": price.price,
            "signal": signal,
            "reason": reason,
            "price_change_24h": change
        })

    return results