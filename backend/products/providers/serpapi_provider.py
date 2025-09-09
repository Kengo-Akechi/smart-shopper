import os
import httpx
from typing import List
from pydantic import ValidationError
from ..schemas import Product
from ..utils import extract_weight_grams, extract_brand, extract_price
from django.conf import settings


BASE_URL = "https://serpapi.com/search.json"


class SerpApiProvider:
    name = "serpapi"

    async def search(self, query: str) -> List[Product]:
        if not settings.SERPAPI_KEY:
            return []
        params = {
            "engine": "google_shopping",
            "q": query,
            "api_key": settings.SERPAPI_KEY,
            "hl": "en",
            "num": "20",
            }
        async with httpx.AsyncClient(http2=True, timeout=settings.REQUEST_TIMEOUT) as client:
            r = await client.get(BASE_URL, params=params)
            r.raise_for_status()
            data = r.json()
        items = data.get("shopping_results", [])
        out: List[Product] = []
        for it in items:
            title = it.get("title")
            price_str = it.get("price")
            price, currency = extract_price(price_str)
            brand = it.get("source") or extract_brand(title)
            wg = extract_weight_grams(title)
            url = it.get("link")
            try:
                out.append(Product(title=title, brand=brand, price=price, currency=currency, weight_grams=wg, source=self.name, url=url))
            except ValidationError:
                continue
        return out