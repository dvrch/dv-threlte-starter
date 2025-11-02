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
    Handles file uploads to Vercel Blob storage.
    Supports both image files and 3D model files (glTF/GLB).
    """
    def post(self, request):
        if 'file' not in request.FILES:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        uploaded_file = request.FILES['file']
        filename = uploaded_file.name
        
        # Déterminer le type de fichier
        ext = filename.lower().split('.')[-1]
        if ext in ['glb', 'gltf']:
            file_type = ext
        elif ext in ['png', 'jpg', 'jpeg', 'gif', 'webp']:
            file_type = 'image'
        else:
            return Response({"error": "Invalid file type. Must be .glb, .gltf, .png, .jpg, .jpeg, .gif, or .webp"}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        print("Token Vercel:", os.environ.get('BLOB_READ_WRITE_TOKEN', 'Non trouvé'))
        
        if not filename:
            return Response({"error": "A 'filename' must be provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Organisation des fichiers par type dans Vercel Blob
        folder = 'models' if file_type in ['gltf', 'glb'] else 'images'
        pathname = f'{folder}/{filename}'
        api_url = f'https://blob.vercel-storage.com?pathname={pathname}'

        try:
            response = requests.post(api_url, headers=headers, data=uploaded_file.read())
            response.raise_for_status()
            
            blob_data = response.json()
            # Ajout du type de fichier dans la réponse pour le frontend
            blob_data['file_type'] = file_type
            return Response(blob_data)

        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Vercel Blob API: {e}")
            return Response({"error": "Failed to communicate with the blob storage service."}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)
