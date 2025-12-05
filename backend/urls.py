import logging

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from django.views.generic import RedirectView

logger = logging.getLogger(__name__)

# Diagnostic view
def health_check(request):
    """Health check endpoint for debugging"""
    response_data = {
        "status": "ok",
        "debug": settings.DEBUG,
        "secret_key_set": bool(settings.SECRET_KEY),
        "allowed_hosts": settings.ALLOWED_HOSTS,
    }

    try:
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        response_data["database"] = "✅ Connected"
        logger.info("Health check: Database connected")
    except Exception as e:
        response_data["database"] = f"❌ Error: {str(e)}"
        logger.error(f"Health check failed: {str(e)}")

    return JsonResponse(response_data)


urlpatterns = [
    # Health check for debugging
    path("health/", health_check, name="health"),
    # Redirection de la racine vers l'API
    path("", RedirectView.as_view(url="/api/", permanent=False)),
    # URLs de l'API - inclure les routeurs des applications
    path("api/", include("backend.films.urls")),
    path("api/", include("backend.Base_threlte_dv.urls")),
    # Interface d'administration
    path("admin/", admin.site.urls),
    path('admin/', admin.site.urls),
]

# Configuration pour servir les fichiers statiques et média en développement
if settings.DEBUG:
    # Servir les fichiers statiques et média en développement
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
