import httpx, bs4
from typing import List, Dict

def fetch() -> List[Dict]:
    qs = ["kpop photocard binder", "western belt buckle", "retro gamer desk toy"]
    out: List[Dict] = []
    with httpx.Client(timeout=20.0, follow_redirects=True) as c:
        for q in qs:
            r = c.get("https://www.ebay.com/sch/i.html?_nkw="+q.replace(" ","+")+"&LH_Sold=1")
            soup = bs4.BeautifulSoup(r.text,"html.parser")
            sold = [e.get_text(strip=True) for e in soup.select(".s-item__title")][:10]
            out.append({"source":"ebay","q":q,"sold_samples":sold})
    return out
