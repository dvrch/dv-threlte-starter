from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Geometry
from .serializers import GeometrySerializer
from rest_framework.views import APIView
from .dv_config import TYPE_CHOICES
import os
import requests

class GeometryViewSet(viewsets.ModelViewSet):
    queryset = Geometry.objects.all()
    serializer_class = GeometrySerializer

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

class HandleBlobUploadView(APIView):
    """
    Handles requests for creating a presigned upload URL for Vercel Blob storage.
    Supports both image files and 3D model files (glTF/GLB).
    """
    def post(self, request):
        print("Données reçues:", request.data)
        
        filename = request.data.get('filename')
        file_type = request.data.get('type', 'image')  # 'image', 'gltf', ou 'glb'
        
        print("Token Vercel:", os.environ.get('BLOB_READ_WRITE_TOKEN', 'Non trouvé'))
        
        if not filename:
            return Response({"error": "A 'filename' must be provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Vérification des types de fichiers autorisés
        if file_type not in ['image', 'gltf', 'glb']:
            return Response({"error": "Invalid file type. Must be 'image', 'gltf', or 'glb'."}, 
                          status=status.HTTP_400_BAD_REQUEST)

        # Vérification de l'extension pour les modèles 3D
        if file_type in ['gltf', 'glb']:
            ext = filename.lower().split('.')[-1]
            if ext not in ['gltf', 'glb']:
                return Response({"error": f"Invalid file extension for {file_type}. Must be .{file_type}"}, 
                              status=status.HTTP_400_BAD_REQUEST)

        token = os.environ.get('BLOB_READ_WRITE_TOKEN')
        if not token:
            print("CRITICAL: BLOB_READ_WRITE_TOKEN is not set.")
            return Response({"error": "Server is not configured for file uploads."}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        headers = {
            'Authorization': f'Bearer {token}',
        }
        
        # Organisation des fichiers par type dans Vercel Blob
        folder = 'models' if file_type in ['gltf', 'glb'] else 'images'
        pathname = f'{folder}/{filename}'
        api_url = f'https://blob.vercel-storage.com?pathname={pathname}'

        try:
            response = requests.post(api_url, headers=headers, json={})
            response.raise_for_status()
            
            blob_data = response.json()
            # Ajout du type de fichier dans la réponse pour le frontend
            blob_data['file_type'] = file_type
            return Response(blob_data)

        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Vercel Blob API: {e}")
            return Response({"error": "Failed to communicate with the blob storage service."}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)
