from pydantic import BaseSettings, AnyUrl
from typing import Optional, List

class Settings(BaseSettings):
    ENV: str = "prod"
    REDIS_URL: str = "redis://redis:6379/0"
    STRIPE_CHECKOUT_LINK: Optional[AnyUrl] = None
    LANDING_HOST: str = "http://localhost:8092"
    STORAGE_DIR: str = "/data"
    SCAN_SOURCES: List[str] = ["producthunt","reddit","tiktok_roundups","etsy","ebay"]
    MIN_TREND_SCORE: float = 0.55
    PORT_API: int = 8087
    class Config:
        env_file = ".env"

settings = Settings()
