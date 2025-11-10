from django.core.cache import cache
import requests

api_key = 'd3v03g1r01qil4as3tsgd3v03g1r01qil4as3tt0'

def _fetch_quote(symbol: str):
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}"
    r = requests.get(url, timeout=5)
    r.raise_for_status()
    j = r.json()
    price = j.get("c")
    prev = j.get("pc") or price
    if not price or price <= 0:
        raise ValueError("No valid price")
    change = price - (prev or price)
    change_pct = (change / prev * 100) if prev else 0.0
    return {
        "symbol": symbol,
        "name": symbol,
        "price": float(price),
        "change": float(change),
        "change_percent": float(change_pct),
    }

def get_stock_price_cached(symbol: str, ttl: int = 90):
    key = f"quote:{symbol.upper()}"
    cached = cache.get(key)
    if cached:
        return cached
    data = _fetch_quote(symbol.upper())
    cache.set(key, data, ttl)
    return data

def get_many_quotes(symbols, ttl: int = 90):
    out = []
    for s in symbols:
        try:
            out.append(get_stock_price_cached(s, ttl=ttl))
        except Exception:
            # If API limit hits, return stale if present, else skip
            stale = cache.get(f"quote:{s.upper()}")
            if stale:
                out.append(stale)
    return out