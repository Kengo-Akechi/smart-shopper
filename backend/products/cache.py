from aiocache import cached


# 60s cache with query key
CACHE_TTL = 60


def cache_key_builder(func, *args, **kwargs):
  q = kwargs.get("query") or (args[1] if len(args) > 1 else "")
  return f"search::{q}"


cached_search = cached(ttl=CACHE_TTL, key_builder=cache_key_builder)