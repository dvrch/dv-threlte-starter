import logging
import os
import re

import requests
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .dv_config import TYPE_CHOICES
from .models import Geometry, BlobLog, B2Asset
from .serializers import GeometrySerializer, B2AssetSerializer

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
        # La sauvegarde initiale gère l'upload du fichier grâce au storage manager
        geometry_instance = serializer.save()
        # Le B2Asset est maintenant créé via l'endpoint d'upload B2 séparé

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class B2AssetViewSet(viewsets.ModelViewSet):
    queryset = B2Asset.objects.all()
    serializer_class = B2AssetSerializer
    pagination_class = None


class TypeView(APIView):
    def get(self, request):
        types = [{"id": choice[0], "name": choice[1]} for choice in TYPE_CHOICES]
        return Response(types)
