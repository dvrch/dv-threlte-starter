from django.contrib import admin
from django.urls import path, include

# from .views import # Assurez-vous d'importer correctement votre vue
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("dashboard/", admin.site.urls),
    path("", include("Base_threlte_dv.urls")),  # Routes de Base_threlte_dv
    path("", include("films.urls")),  # Routes des films
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# -------------
