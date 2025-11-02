from django.contrib import admin
from django.urls import path, include

# from .views import # Assurez-vous d'importer correctement votre vue
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from films.views import FilmViewSet
from Base_threlte_dv.views import GeometryViewSet, TypeView, HandleBlobUploadView

# Création d'un routeur principal pour toutes les APIs
router = DefaultRouter()
router.register(r'films', FilmViewSet, basename='films')
router.register(r'geometries', GeometryViewSet, basename='geometries')

from django.views.generic import RedirectView

urlpatterns = [
    # Redirection de la racine vers l'API
    path('', RedirectView.as_view(url='/api/', permanent=False)),
    
    # URLs de l'API
    path('api/', include(router.urls)),  # Toutes les APIs REST sous /api/
    path('api/types/', TypeView.as_view(), name='types'),
    path('api/upload/', HandleBlobUploadView.as_view(), name='handle-upload'),
    
    # Interface d'administration
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# -------------
