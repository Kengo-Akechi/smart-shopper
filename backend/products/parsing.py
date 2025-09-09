from typing import List
from .schemas import Product


# De‑duplication and normalization helpers


def dedupe(products: List[Product]) -> List[Product]:
    seen = set()
    out = []
    for p in products:
        key = (p.title.lower(), p.brand or "", round(p.price or -1, 2))
        if key in seen:
            continue
        seen.add(key)
        out.append(p)
    return out


def sort_results(products: List[Product]) -> List[Product]:
    return sorted(products, key=lambda p: (p.price if p.price is not None else 1e12))