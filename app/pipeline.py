from typing import List, Dict
from .schemas import Trend

def heuristics(cluster: List[Dict]) -> List[Trend]:
    out: List[Trend] = []
    for row in cluster:
        txt = " ".join([str(v).lower() for v in row.values()])
        if any(w in txt for w in ["image","lifestyle","ai"]):
            out.append(Trend(trend="AI product-lifestyle image generators",
                             urgency_score=9, revenue_potential="$5k–$30k/mo",
                             automation_plan="SaaS for Etsy/Shopify images", meta=row))
        elif "video" in txt or "upscale" in txt:
            out.append(Trend(trend="AI video upscaling for creators",
                             urgency_score=8, revenue_potential="$2k–$15k/mo",
                             automation_plan="credit-based queue", meta=row))
        elif any(w in txt for w in ["k-pop","photocard","western","bolo","belt"]):
            out.append(Trend(trend="K-pop/Western aesthetic accessories",
                             urgency_score=7, revenue_potential="$1k–$8k/mo",
                             automation_plan="Etsy/TikTok shop", meta=row))
        elif any(w in txt for w in ["kojic","lip stain","k-beauty","rejuran","salmon dna"]):
            out.append(Trend(trend="UGC-led beauty micro-SKUs",
                             urgency_score=6, revenue_potential="$2k–$12k/mo",
                             automation_plan="curated dropship", meta=row))
    dedup = {}
    for t in out:
        if t.trend not in dedup:
            dedup[t.trend] = t
    return list(dedup.values())

from pytrends.request import TrendReq

def validate_with_google_trends(candidates: List[Trend]) -> List[Trend]:
    keys=[c.trend for c in candidates]
    pytrends = TrendReq(hl="en-US", tz=0)
    scores={}
    for i in range(0, len(keys), 5):
        kw = keys[i:i+5]
        try:
            pytrends.build_payload(kw, timeframe="now 7-d", geo="")
            df = pytrends.interest_over_time()
            if df is None or df.empty:
                for k in kw: scores[k]=0.0
                continue
            window = df.tail(24).mean(numeric_only=True)
            for k in kw:
                scores[k] = float(window.get(k, 0.0))/100.0
        except Exception:
            for k in kw: scores[k]=0.0
    kept=[]
    for c in candidates:
        gt = scores.get(c.trend, 0.0)
        if gt >= 0.20:
            c.meta["google_trends_score"]=gt
            kept.append(c)
    return kept
