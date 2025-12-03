from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

# from .views import # Assurez-vous d'importer correctement votre vue
from django.conf import settings
from django.conf.urls.static import static

# Diagnostic view
def health_check(request):
    """Health check endpoint for debugging"""
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        db_status = "✅ Database connected"
    except Exception as e:
        db_status = f"❌ Database error: {str(e)}"
    
    return JsonResponse({
        "status": "ok",
        "database": db_status,
        "debug": settings.DEBUG,
        "secret_key_set": bool(settings.SECRET_KEY),
    })

from rest_framework.routers import DefaultRouter
from films.views import FilmViewSet
try:
    # Try relative import first (works when Django starts from backend/ folder locally)
    from Base_threlte_dv.views import GeometryViewSet, TypeView
except ImportError:
    try:
        # Fall back to absolute import (works on Vercel when Django starts from project root)
        from backend.Base_threlte_dv.views import GeometryViewSet, TypeView
    except ImportError:
        # Last resort - add backend to path and try again
        import sys
        from pathlib import Path
        backend_path = Path(__file__).resolve().parent
        if str(backend_path) not in sys.path:
            sys.path.insert(0, str(backend_path))
        from Base_threlte_dv.views import GeometryViewSet, TypeView

# Création d'un routeur principal pour toutes les APIs
router = DefaultRouter()
router.register(r'films', FilmViewSet, basename='films')
router.register(r'geometries', GeometryViewSet, basename='geometries')

from django.views.generic import RedirectView

urlpatterns = [
    # Health check for debugging
    path('health/', health_check, name='health'),
    
    # Redirection de la racine vers l'API
    path('', RedirectView.as_view(url='/api/', permanent=False)),
    
    # URLs de l'API
    path('api/', include(router.urls)),  # Toutes les APIs REST sous /api/
    path('api/types/', TypeView.as_view(), name='types'),
    
    
    # Interface d'administration
    path('admin/', admin.site.urls),
]

# Configuration pour servir les fichiers statiques et média en développement
if settings.DEBUG:
    # Servir les fichiers statiques et média en développement
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# -------------
