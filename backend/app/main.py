from fastapi import FastAPI
from app.kalshi import get_fade_opportunities

app = FastAPI()

@app.get("/fade-opportunities")
def fade_opportunities():
    try:
        opportunities = get_fade_opportunities()
        return {"opportunities": opportunities}
    except Exception as e:
        print(f"[ERROR] {e}")
        return {"error": str(e)}
