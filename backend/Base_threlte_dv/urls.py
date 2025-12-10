import os
from django.conf import settings
from django.http import JsonResponse
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GeometryViewSet, TypeView


def debug_env(request):
    """Debug endpoint to check environment variables"""
    env_vars = {
        "USE_CLOUDINARY": os.environ.get("USE_CLOUDINARY"),
        "CLOUDINARY_CLOUD_NAME": os.environ.get("CLOUDINARY_CLOUD_NAME"),
        "CLOUDINARY_API_KEY": os.environ.get("CLOUDINARY_API_KEY"),
        "CLOUDINARY_API_SECRET": "SET"
        if os.environ.get("CLOUDINARY_API_SECRET")
        else "NOT SET",
        "DEFAULT_FILE_STORAGE": getattr(settings, "DEFAULT_FILE_STORAGE", None),
        "CLOUDINARY_STORAGE": getattr(settings, "CLOUDINARY_STORAGE", None),
    }
    return JsonResponse(env_vars)


router = DefaultRouter()
router.register("geometries", GeometryViewSet, basename="geometries")

urlpatterns = [
    path("types/", TypeView.as_view(), name="types"),
    path("debug-env/", debug_env, name="debug-env"),
    path("", include(router.urls)),
]
