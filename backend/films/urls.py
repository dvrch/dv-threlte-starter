from django.urls import path 
from films.views import FilmViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'films', FilmViewSet, basename='films')
urlpatterns = router.urls
