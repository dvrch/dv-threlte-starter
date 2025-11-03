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
    En développement, les fichiers sont également sauvegardés localement pour backup.
    """
    def post(self, request):
        response = None
        try:
            if 'file' not in request.FILES:
                return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

            uploaded_file = request.FILES['file']
            filename = uploaded_file.name
            
            if not filename:
                return Response({"error": "A 'filename' must be provided."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Déterminer le type de fichier
            ext = filename.lower().split('.')[-1]
            if ext in ['glb', 'gltf']:
                file_type = ext
            elif ext in ['png', 'jpg', 'jpeg', 'gif', 'webp']:
                file_type = 'image'
            else:
                return Response({"error": "Invalid file type. Must be .glb, .gltf, .png, .jpg, .jpeg, .gif, or .webp"}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            # Lire le contenu du fichier une seule fois
            file_content = uploaded_file.read()
            
            # Vérifier la configuration du token Blob Storage
            token = os.environ.get('BLOB_READ_WRITE_TOKEN')
            if not token:
                # En développement sans token, sauvegarder localement
                if settings.DEBUG:
                    import uuid
                    from pathlib import Path
                    
                    # Sauvegarder localement en développement
                    folder = 'models' if file_type in ['gltf', 'glb'] else 'images'
                    media_folder = settings.MEDIA_ROOT / folder
                    media_folder.mkdir(parents=True, exist_ok=True)
                    
                    # Nettoyer le nom de fichier même pour le stockage local
                    clean_filename_local = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
                    clean_filename_local = re.sub(r'_+', '_', clean_filename_local)
                    
                    # Générer un nom unique pour éviter les collisions
                    unique_filename = f"{uuid.uuid4().hex[:8]}_{clean_filename_local}"
                    file_path = media_folder / unique_filename
                    
                    with open(file_path, 'wb') as f:
                        f.write(file_content)
                    
                    # Retourner l'URL locale
                    media_url = f"{settings.MEDIA_URL}{folder}/{unique_filename}"
                    return Response({
                        "url": request.build_absolute_uri(media_url),
                        "pathname": f"{folder}/{unique_filename}",
                        "filename": unique_filename,
                        "file_type": file_type,
                        "message": "File saved locally (Blob Storage not configured)"
                    })
                else:
                    print("CRITICAL: BLOB_READ_WRITE_TOKEN is not set.")
                    return Response({"error": "Server is not configured for file uploads."}, 
                                  status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Upload vers Vercel Blob Storage
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': uploaded_file.content_type
            }
            
            # Organisation des fichiers par type dans Vercel Blob
            # Encoder le nom de fichier pour éviter les caractères invalides dans l'URL
            # Nettoyer le nom de fichier (supprimer les caractères spéciaux, garder seulement alphanumériques, tirets, points et underscores)
            clean_filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
            # Remplacer les underscores multiples par un seul underscore
            clean_filename = re.sub(r'_+', '_', clean_filename)
            
            folder = 'models' if file_type in ['gltf', 'glb'] else 'images'
            pathname = f'{folder}/{filename}'
            api_url = f'https://blob.vercel-storage.com/{pathname}'

            print(f"Attempting to upload to Vercel Blob. API URL: {api_url}, Filename: {filename}, File type: {file_type}")

            try:
                # Upload vers Vercel Blob
                response = requests.put(api_url, headers=headers, data=file_content, timeout=30)
                response.raise_for_status()
                
                blob_data = response.json()
                blob_data['file_type'] = file_type
                blob_data['filename'] = clean_filename  # Utiliser le nom nettoyé dans la réponse
                
                # En développement, également sauvegarder localement comme backup
                if settings.DEBUG:
                    try:
                        from pathlib import Path
                        media_folder = settings.MEDIA_ROOT / folder
                        media_folder.mkdir(parents=True, exist_ok=True)
                        file_path = media_folder / clean_filename  # Utiliser le nom nettoyé
                        with open(file_path, 'wb') as f:
                            f.write(file_content)
                    except Exception as backup_error:
                        print(f"Warning: Could not save local backup: {backup_error}")
                
                return Response(blob_data)

            except requests.exceptions.Timeout:
                return Response({"error": "Upload timeout. The file may be too large."}, 
                              status=status.HTTP_408_REQUEST_TIMEOUT)
            except requests.exceptions.RequestException as e:
                import traceback
                print(f"Error communicating with Vercel Blob API: {e}")
                if response is not None:
                    print(f"Vercel Blob API Response Status Code: {response.status_code}")
                    print(f"Vercel Blob API Response Text: {response.text}")
                traceback.print_exc()
                return Response({"error": "Failed to communicate with the blob storage service."}, 
                              status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            import traceback
            print(f"An unexpected error occurred in HandleBlobUploadView: {e}")
            traceback.print_exc()
            return Response({"error": "An unexpected server error occurred."}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)
