import os
from .KalshiClientsBaseV2ApiKey import ExchangeClient
from .redis_cache import cache_get, cache_set, load_private_key

KALSHI_ENV = os.getenv("KALSHI_ENV", "PROD")
KALSHI_HOST = "https://trading-api.kalshi.com/trade-api/v2" if KALSHI_ENV == "PROD" else "https://demo-api.kalshi.co/trade-api/v2"

def get_fade_opportunities():
    try:
        key_id = os.getenv("KALSHI_KEY_ID")
        private_key = load_private_key()

        client = ExchangeClient(
            exchange_api_base=KALSHI_HOST,
            key_id=key_id,
            private_key=private_key,
        )

        cached_data = cache_get("sports_fade_opportunities")
        if cached_data:
            return cached_data

        all_markets = client.get_markets(status="open")
        sports = [m for m in all_markets["markets"] if m["ticker"].startswith("SP")]
        fade_opportunities = []

        for market in sports:
            yes_bid = market.get("yes_bid")
            no_bid = market.get("no_bid")
            if yes_bid is None or no_bid is None:
                continue
            if yes_bid > 51:
                fade_opportunities.append({"fade": "yes", "market": market})
            elif no_bid > 51:
                fade_opportunities.append({"fade": "no", "market": market})

        cache_set("sports_fade_opportunities", fade_opportunities)
        return fade_opportunities

    except Exception as e:
        return {"error": str(e)}
