import httpx, bs4
from typing import List, Dict

def fetch() -> List[Dict]:
    qs = ["western belt", "bolo tie clip", "photocard binder", "kojic acid serum label"]
    out: List[Dict] = []
    with httpx.Client(timeout=20.0, follow_redirects=True) as c:
        for q in qs:
            r = c.get("https://www.etsy.com/search?q="+q.replace(" ","+"))
            soup = bs4.BeautifulSoup(r.text,"html.parser")
            titles = [e.get_text(strip=True) for e in soup.select("h3")]
            out.append({"source":"etsy","q":q,"hits":titles[:8]})
    return out
