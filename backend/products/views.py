import asyncio
from django.http import JsonResponse, HttpRequest
from django.conf import settings
from .utils import normalize_query
from .schemas import Product
from .parsing import dedupe, sort_results
from .providers.serpapi_provider import SerpApiProvider
from .providers.google_html_provider import GoogleHtmlProvider
from .cache import cached_search


# Assemble providers – order matters (fastest/most reliable first)
PROVIDERS = [SerpApiProvider(), GoogleHtmlProvider()]


async def _gather_with_concurrency(n, *tasks):
    sem = asyncio.Semaphore(n)
    async def sem_task(coro)