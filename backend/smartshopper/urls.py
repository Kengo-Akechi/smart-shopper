from django.urls import path, include


urlpatterns = [
path("api/products/", include("products.urls")),
]