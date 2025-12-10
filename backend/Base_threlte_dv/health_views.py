from django.http import JsonResponse
from django.conf import settings
from rest_framework.views import APIView


class HealthCheckView(APIView):
    def get(self, request):
        """Vérifier l'état de santé et la configuration Cloudinary"""
        return JsonResponse(
            {
                "status": "ok",
                "debug": settings.DEBUG,
                "use_cloudinary": getattr(settings, "USE_CLOUDINARY", False),
                "cloudinary_config": {
                    "cloud_name": getattr(settings, "CLOUDINARY_STORAGE", {}).get(
                        "CLOUD_NAME", None
                    ),
                    "has_api_key": bool(
                        getattr(settings, "CLOUDINARY_STORAGE", {}).get("API_KEY", None)
                    ),
                    "has_api_secret": bool(
                        getattr(settings, "CLOUDINARY_STORAGE", {}).get(
                            "API_SECRET", None
                        )
                    ),
                },
                "default_file_storage": str(settings.DEFAULT_FILE_STORAGE),
            }
        )
