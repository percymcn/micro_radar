from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict, Any

class Trend(BaseModel):
    trend: str
    urgency_score: int
    revenue_potential: str
    automation_plan: str
    meta: Dict[str, Any] = {}

class ScanResult(BaseModel):
    items: List[Trend]

class DeployRequest(BaseModel):
    trend: Trend
    slug: str
    price_cents: int = 2900
    checkout_url: Optional[HttpUrl] = None
