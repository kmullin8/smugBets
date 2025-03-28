from pydantic import BaseModel

class FadeOpportunity(BaseModel):
    ticker: str
    title: str
    yes_price: int
    no_price: int
    public_yes_pct: float
