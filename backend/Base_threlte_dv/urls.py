from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GeometryViewSet, TypeView, HandleBlobUploadView

router = DefaultRouter()
router.register('geometries', GeometryViewSet, basename='geometries')

urlpatterns = [
    path('types/', TypeView.as_view(), name='types'),
    path('handle-upload/', HandleBlobUploadView.as_view(), name='handle-upload'),
    path('', include(router.urls)),
]
