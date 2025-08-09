import httpx, bs4
from typing import List, Dict

URLS = [
    "https://www.producthunt.com/leaderboard/daily/2025/8/5",
    "https://www.producthunt.com/leaderboard/daily/2025/8/1",
    "https://www.producthunt.com/leaderboard/monthly/2025/8/all",
]

def fetch() -> List[Dict]:
    out: List[Dict] = []
    with httpx.Client(timeout=20.0, follow_redirects=True) as c:
        for url in URLS:
            r = c.get(url)
            soup = bs4.BeautifulSoup(r.text, "html.parser")
            for img in soup.select("img[alt]"):
                name = (img.get("alt") or "").strip()
                if not name: continue
                low = name.lower()
                if any(k in low for k in ["ai", "image", "video", "local", "privacy"]):
                    out.append({"source":"producthunt","name":name,"url":url})
    return out
