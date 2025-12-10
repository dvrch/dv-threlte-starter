from django.http import JsonResponse
from django.conf import settings
import os


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
