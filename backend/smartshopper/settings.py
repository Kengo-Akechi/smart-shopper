import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-key")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
ALLOWED_HOSTS = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "*").split(",")]


INSTALLED_APPS = [
"django.contrib.contenttypes",
"django.contrib.staticfiles",
"products",
]


MIDDLEWARE = [
"django.middleware.common.CommonMiddleware",
]


ROOT_URLCONF = "smartshopper.urls"
TEMPLATES = []
WSGI_APPLICATION = "smartshopper.wsgi.application"
ASGI_APPLICATION = "smartshopper.asgi.application"


DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}


STATIC_URL = "/static/"


# Caching (Redis) – used by aiocache
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
AIOCACHE_DEFAULTS = {
"cache": "aiocache.RedisCache",
"endpoint": os.getenv("REDIS_HOST", "redis"),
"port": int(os.getenv("REDIS_PORT", 6379)),
"timeout": 1,
"serializer": {"class": "aiocache.serializers.PickleSerializer"},
}


# External keys
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", 3.0))
CONCURRENCY = int(os.getenv("CONCURRENCY", 10))