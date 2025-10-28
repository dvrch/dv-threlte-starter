from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GeometryViewSet, TypeView

router = DefaultRouter()
router.register('geometries', GeometryViewSet, basename='geometries')

urlpatterns = [
    path('types/', TypeView.as_view(), name='types'),
    path('', include(router.urls)),
]
