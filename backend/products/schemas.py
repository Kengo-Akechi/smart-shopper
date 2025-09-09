from pydantic import BaseModel, Field
from typing import Optional


class Product(BaseModel):
  title: str
  brand: str | None = None
  price: float | None = None
  currency: str | None = None
  weight_grams: float | None = Field(default=None, description="Weight in grams")
  source: str
  url: Optional[str] = None