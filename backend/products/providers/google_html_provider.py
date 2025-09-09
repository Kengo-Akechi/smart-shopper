import httpx
from bs4 import BeautifulSoup
from typing import List
from ..schemas import Product
from ..utils import extract_weight_grams, extract_brand, extract_price
from django.conf import settings


# NOTE: Direct scraping of Google may violate their ToS and can be rate-limited or blocked.
# Prefer SerpAPI in production. This provider is a best-effort fallback for demo/testing.


HEADERS = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
}


class GoogleHtmlProvider:
    name = "google_html"
    
    async def search(self, query: str) -> List[Product]:
        q = query.replace(" ", "+")
        url = f"https://www.google.com/search?tbm=shop&q={q}"
        async with httpx.AsyncClient(headers=HEADERS, http2=True, timeout=settings.REQUEST_TIMEOUT, follow_redirects=True) as client:
            r = await client.get(url)
            r.raise_for_status()
            html = r.text
        soup = BeautifulSoup(html, "lxml")
        cards = soup.select("div.sh-dgr__content")
        results: List[Product] = []
        for c in cards[:20]:
            title_el = c.select_one("h3, div[class*='product-title']")
            title = title_el.get_text(strip=True) if title_el else None
            price_el = c.select_one("span[aria-label*='$'], span[aria-label*='₹'], span:contains('$')")
            price_text = price_el.get_text(strip=True) if price_el else None
            price, currency = extract_price(price_text)
            brand = extract_brand(title)
            weight = extract_weight_grams(title)
            link_el = c.select_one("a[href]")
            url = ("https://www.google.com" + link_el["href"]) if link_el else None
            if not title:
                continue
            results.append(Product(title=title, brand=brand, price=price, currency=currency, weight_grams=weight, source=self.name, url=url))
        return results