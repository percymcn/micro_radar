import httpx
from typing import List, Dict

SUBS = ["Entrepreneur","smallbusiness","SideProject"]

def fetch() -> List[Dict]:
    items: List[Dict] = []
    headers = {"User-Agent":"micro-radar/0.1"}
    with httpx.Client(timeout=20.0, headers=headers) as c:
        for sub in SUBS:
            url = f"https://www.reddit.com/r/{sub}/hot.json?limit=25"
            r = c.get(url)
            if r.status_code != 200: continue
            data = r.json().get("data",{}).get("children",[])
            for p in data:
                d = p.get("data",{})
                title = d.get("title","")
                low = title.lower()
                if any(k in low for k in ["trend","launch","product","shop","tiktok","etsy","ai"]):
                    items.append({"source":"reddit","title":title,"permalink":"https://reddit.com"+d.get("permalink","")})
    return items
