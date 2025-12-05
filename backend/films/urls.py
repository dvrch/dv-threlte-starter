from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import FilmViewSet

router.register(r"films", FilmViewSet, basename="films")
router.register(r'films', FilmViewSet, basename='films')
urlpatterns = router.urls
