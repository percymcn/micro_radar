# Not scraping TikTok directly; parse stable roundup pages.
import httpx, bs4
from typing import List, Dict

ROUNDUPS = [
    "https://newsroom.tiktok.com/en-gb/tiktok-shopping-report",
    "https://www.ramd.am/blog/trends-tiktok",
]

def fetch() -> List[Dict]:
    out: List[Dict] = []
    with httpx.Client(timeout=20.0, follow_redirects=True) as c:
        for url in ROUNDUPS:
            r = c.get(url)
            soup = bs4.BeautifulSoup(r.text, "html.parser")
            text = soup.get_text(" ", strip=True).lower()
            for kw in ["lip stain","k-beauty","rejuran","salmon dna","k-pop","photocard","dupe","viral"]:
                if kw in text:
                    out.append({"source":"tiktok_roundups","keyword":kw,"url":url})
    return out
