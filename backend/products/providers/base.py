from typing import List
from ..schemas import Product


class BaseProvider:
  name = "base"
  async def search(self, query: str) -> List[Product]:
    raise NotImplementedError