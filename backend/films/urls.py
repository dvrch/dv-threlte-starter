# backend/films/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FilmViewSet

# Create a router
router = DefaultRouter()
router.register(r"films", FilmViewSet, basename="films")

# URL patterns
urlpatterns = [
    path("", include(router.urls)),
]
