from fastapi import FastAPI
from app.kalshi import get_fade_opportunities
from app.redis_cache import cache_get, cache_set

app = FastAPI()

@app.get("/fade-opportunities")
async def fade_opportunities():
    cached = cache_get("fade_opportunities")
    if cached:
        return cached
    opportunities = get_fade_opportunities()
    cache_set("fade_opportunities", opportunities, ex=120)
    return opportunities
