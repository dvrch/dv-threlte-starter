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

    def partial_update(self, request, *args, **kwargs):
        logger.info(f"--- Entering partial_update for Geometry ID: {kwargs.get('pk')} ---")
        logger.info(f"Request data: {request.data}")
        try:
            response = super().partial_update(request, *args, **kwargs)
            logger.info(f"Update successful. Response status: {response.status_code}")
            return response
        except Exception as e:
            logger.error(f"!!! EXCEPTION in partial_update: {str(e)}", exc_info=True)
            # Re-raise the exception to let DRF handle the error response
            raise

    def perform_create(self, serializer):
        # La sauvegarde initiale gère l'upload du fichier grâce au serializer
        geometry_instance = serializer.save()

        # Si une URL de modèle a été générée, créer l'enregistrement CloudinaryAsset
        if geometry_instance.model_url:
            # Extraire le public_id depuis l'URL Cloudinary
            url_pattern = r"/dv-threlte/models/([^/]+)"
            match = re.search(url_pattern, geometry_instance.model_url)

            if match:
                public_id = f"dv-threlte/models/{match.group(1)}"

                # Créer ou mettre à jour l'enregistrement de l'asset
                asset, created = CloudinaryAsset.objects.update_or_create(
                    public_id=public_id,
                    defaults={
                        "url": geometry_instance.model_url,
                        "asset_type": "raw",
                        "file_name": geometry_instance.name or public_id.split("/")[-1],
                        "file_size": 0,  # Size not available from URL
                    },
                )
                logger.info(
                    f"✅ {'Created' if created else 'Updated'} CloudinaryAsset: {public_id}"
                )

        logger.info(f"✅ Created geometry: {geometry_instance.name}")
        return geometry_instance

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Supprimer le fichier Cloudinary associé
        if instance.model_url:
            try:
                # Extraire le public_id depuis l'URL
                url_pattern = r"/dv-threlte/models/([^/]+)"
                match = re.search(url_pattern, instance.model_url)

                if match:
                    public_id = f"dv-threlte/models/{match.group(1)}"

                    # Supprimer l'asset de Cloudinary
                    import cloudinary.uploader

                    cloudinary.uploader.destroy(public_id, resource_type="raw")
                    logger.info(f"✅ Deleted Cloudinary asset: {public_id}")

                    # Supprimer l'enregistrement CloudinaryAsset correspondant
                    from .models import CloudinaryAsset

                    CloudinaryAsset.objects.filter(public_id=public_id).delete()
                    logger.info(f"✅ Deleted CloudinaryAsset record: {public_id}")

            except Exception as e:
                logger.error(f"❌ Error deleting Cloudinary asset: {str(e)}")

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ToggleGeometryVisibilityView(APIView):
    def patch(self, request, pk):
        try:
            geometry = Geometry.objects.get(pk=pk)
            geometry.visible = not geometry.visible
            geometry.save()

            return Response(
                {
                    "id": geometry.id,
                    "visible": geometry.visible,
                    "message": f"Géométrie {'activée' if geometry.visible else 'désactivée'}",
                }
            )
        except Geometry.DoesNotExist:
            return Response(
                {"error": "Géométrie non trouvée"}, status=status.HTTP_404_NOT_FOUND
            )


class TypeView(APIView):
    def get(self, request):
        types = [{"id": choice[0], "name": choice[1]} for choice in TYPE_CHOICES]
        return Response(types)
