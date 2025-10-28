from django.contrib import admin
from django.urls import path, include
# from .views import # Assurez-vous d'importer correctement votre vue
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('Base_threlte_dv.urls')), # Ajout de la route pour les films
    path('api/', include('films.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# -------------





