from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Geometry
from .serializers import GeometrySerializer
from rest_framework.views import APIView
from .dv_config import TYPE_CHOICES
from django.conf import settings
from urllib.parse import quote
import os
import re
import requests

class GeometryViewSet(viewsets.ModelViewSet):
    queryset = Geometry.objects.all()
    serializer_class = GeometrySerializer

    def _upload_to_blob(self, file):
        token = os.environ.get('BLOB_READ_WRITE_TOKEN')
        if not token:
            # Gérer le cas où le token n'est pas défini (par exemple, en développement local)
            # Vous pouvez retourner une URL locale ou lever une exception
            return None

        filename = file.name
        clean_filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
        clean_filename = re.sub(r'_+', '_', clean_filename)
        
        ext = filename.lower().split('.')[-1]
        folder = 'models' if ext in ['gltf', 'glb'] else 'images'
        pathname = f'{folder}/{clean_filename}'
        api_url = f'https://blob.vercel-storage.com/{pathname}'

        headers = {'Authorization': f'Bearer {token}'}
        response = requests.put(api_url, headers=headers, data=file.read())
        response.raise_for_status()
        return response.json().get('url')

    def perform_create(self, serializer):
        model_file = self.request.data.get('model_file')
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
        model_file = self.request.data.get('model_file')
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
        types = [{'id': choice[0], 'name': choice[1]} for choice in TYPE_CHOICES]
        return Response(types)


