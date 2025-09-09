import re


def normalize_query(q: str) -> str:
  return re.sub(r"\s+", " ", q.strip()).lower()


_WEIGHT_RE = re.compile(r"(\d+(?:[\.,]\d+)?)\s*(kg|g|lb|oz)", re.I)


def extract_weight_grams(text: str) -> float | None:
  if not text:
    return None
  m = _WEIGHT_RE.search(text)
  if not m:
    return None
  qty = float(m.group(1).replace(",", "."))
  unit = m.group(2).lower()
  if unit == "g":
    return qty
  if unit == "kg":
    return qty * 1000
  if unit == "lb":
    return qty * 453.59237
  if unit == "oz":
   return qty * 28.349523125
  return None


_PRICE_RE = re.compile(r"([\$€£₹])\s*(\d+[\d,]*(?:\.\d{1,2})?)")


def extract_price(text: str) -> tuple[float | None, str | None]:
  if not text:
   return None, None
  m = _PRICE_RE.search(text)
  if not m:
    return None, None
  sym, amt = m.groups()
  amt = float(amt.replace(",", ""))
  return amt, sym


_BRAND_RE = re.compile(r"\b(365|whole\s*foods|wholefoods|kirkland|great\s*value|organic)\b", re.I)


def extract_brand(text: str) -> str | None:
  if not text:
   return None
  m = _BRAND_RE.search(text)
  return m.group(1) if m else None