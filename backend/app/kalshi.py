import os
from app.models import FadeOpportunity
from app.redis_cache import load_private_key
from .KalshiClientsBaseV2ApiKey import ExchangeClient

# Load from .env
from dotenv import load_dotenv
load_dotenv()

KALSHI_KEY_ID = os.getenv("KALSHI_KEY_ID")
PRIVATE_KEY_PATH = os.getenv("KALSHI_PRIVATE_KEY_PATH")
PROD_URL = "https://api.elections.kalshi.com/trade-api/v2"

def get_fade_opportunities():
    private_key = load_private_key(PRIVATE_KEY_PATH)
    client = ExchangeClient(PROD_URL, key_id=KALSHI_KEY_ID, private_key=private_key)
    result = client.get_markets(status="open")
    opportunities = []

    for market in result.get("markets", []):
        yes_price = market.get("yes_price", 0)
        no_price = market.get("no_price", 0)
        if not yes_price or not no_price:
            continue

        sentiment = round((yes_price / (yes_price + no_price)) * 100, 2)
        if sentiment > 51:
            opportunities.append(FadeOpportunity(
                ticker=market["ticker"],
                title=market["title"],
                yes_price=yes_price,
                no_price=no_price,
                public_yes_pct=sentiment
            ))

    return [op.dict() for op in opportunities]
