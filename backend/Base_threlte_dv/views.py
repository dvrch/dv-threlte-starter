import logging
import logging
import os
import re

import requests
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .dv_config import TYPE_CHOICES
from .models import Geometry, BlobLog, CloudinaryAsset
from .serializers import GeometrySerializer

logger = logging.getLogger(__name__)


class GeometryViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        try:
            logger.info("✅ GeometryViewSet.list() called")
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"❌ Error in GeometryViewSet.list(): {str(e)}", exc_info=True)
            raise

    queryset = Geometry.objects.all()
    serializer_class = GeometrySerializer
    pagination_class = None

    def perform_create(self, serializer):
        # La sauvegarde initiale gère l'upload du fichier grâce à `django-cloudinary-storage`
        geometry_instance = serializer.save()

        # Si un fichier a été uploadé, `model_file` sera présent sur l'instance
        if geometry_instance.model_file and hasattr(
            geometry_instance.model_file, "public_id"
        ):
            # Créer ou mettre à jour l'enregistrement de l'asset
            asset, created = CloudinaryAsset.objects.update_or_create(
                public_id=geometry_instance.model_file.public_id,
                defaults={
                    "asset_id": getattr(geometry_instance.model_file, "asset_id", None),
                    "url": geometry_instance.model_file.url,
                    "asset_type": "raw",
                    "file_name": geometry_instance.model_file.name,
                    "file_size": geometry_instance.model_file.size,
                },
            )
            # Lier l'asset à l'instance de géométrie et sauvegarder
            geometry_instance.asset = asset
            geometry_instance.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TypeView(APIView):
    def get(self, request):
        types = [{"id": choice[0], "name": choice[1]} for choice in TYPE_CHOICES]
        return Response(types)
