import logging
import logging
import os
import re

import requests
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .dv_config import TYPE_CHOICES
from .models import Geometry
from .serializers import GeometrySerializer

logger = logging.getLogger(__name__)


class GeometryViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        try:
            logger.info("✅ GeometryViewSet.list() called - DEBUG MODE")
            # Temporarily bypass the database to test the API route
            dummy_data = [
                {
                    "id": 1,
                    "name": "Debug Cube",
                    "type": "CUBE",
                    "model_url": "https://example.com/cube.glb",
                },
                {
                    "id": 2,
                    "name": "Debug Sphere",
                    "type": "SPHERE",
                    "model_url": "https://example.com/sphere.glb",
                },
            ]
            return Response(dummy_data, status=status.HTTP_200_OK)
            # logger.info("✅ GeometryViewSet.list() called")
            # return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"❌ Error in GeometryViewSet.list(): {str(e)}", exc_info=True)
            raise

    queryset = Geometry.objects.all()
    serializer_class = GeometrySerializer

    def _upload_to_blob(self, file):
        token = os.environ.get("BLOB_READ_WRITE_TOKEN")
        if not token:
            # Gérer le cas où le token n'est pas défini (par exemple, en développement local)
            # Vous pouvez retourner une URL locale ou lever une exception
            return None

        filename = file.name
        clean_filename = re.sub(r"[^a-zA-Z0-9._-]", "_", filename)
        clean_filename = re.sub(r"_+", "_", clean_filename)

        ext = filename.lower().split(".")[-1]
        folder = "models" if ext in ["gltf", "glb"] else "images"
        pathname = f"{folder}/{clean_filename}"
        api_url = f"https://blob.vercel-storage.com/{pathname}"

        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(api_url, headers=headers, data=file.read())
        response.raise_for_status()
        return response.json().get("url")

    def perform_create(self, serializer):
        model_file = self.request.data.get("model_file")
        if model_file:
            blob_url = self._upload_to_blob(model_file)
            if blob_url:
                serializer.save(model_url=blob_url)
            else:
                # Gérer l'échec de l'upload si nécessaire
                serializer.save()
        else:
            serializer.save()

    def perform_update(self, serializer):
        model_file = self.request.data.get("model_file")
        if model_file:
            blob_url = self._upload_to_blob(model_file)
            if blob_url:
                serializer.save(model_url=blob_url)
            else:
                serializer.save()
        else:
            serializer.save()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TypeView(APIView):
    def get(self, request):
        types = [{"id": choice[0], "name": choice[1]} for choice in TYPE_CHOICES]
        return Response(types)
