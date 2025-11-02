from django.contrib import admin
from django.conf import settings

# Personnalisation de l'interface d'administration
admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.index_title = settings.ADMIN_INDEX_TITLE
