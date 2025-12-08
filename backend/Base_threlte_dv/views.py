import logging
import logging
import os
import re

import requests
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .dv_config import TYPE_CHOICES
from .models import Geometry, BlobLog
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

    def _upload_to_blob(self, file_obj):
        """
        Uploads a file to Vercel Blob Storage.
        Returns the public URL of the uploaded blob.
        """
        # On récupère le token depuis les variables d'environnement
        # (chargées via dotenv ou l'environnement système)
        token = os.environ.get("BLOB_READ_WRITE_TOKEN")
        
        if not token:
            logger.warning("⚠️ BLOB_READ_WRITE_TOKEN not found. Falling back to local storage.")
            return None

        try:
            filename = file_obj.name
            # Nettoyage simple du nom de fichier
            clean_filename = re.sub(r"[^a-zA-Z0-9._-]", "_", filename)
            
            # Déterminer le dossier
            ext = filename.lower().split(".")[-1]
            folder = "models" if ext in ["gltf", "glb"] else "images"
            pathname = f"{folder}/{clean_filename}"
            
            # Appel à l'API de Vercel Blob
            api_url = f"https://blob.vercel-storage.com/{pathname}"
            headers = {
                "Authorization": f"Bearer {token}",
                # On ne met pas Content-Type ici, requests le gérera ou Vercel le détectera
            }
            
            logger.info(f"📤 Uploading {filename} to Vercel Blob as {pathname}...")
            
            # Important: lire le contenu du fichier
            file_content = file_obj.read()
            file_size = len(file_content)
            
            # put request
            response = requests.put(api_url, headers=headers, data=file_content)
            response.raise_for_status()
            
            data = response.json()
            blob_url = data.get("url")
            
            logger.info(f"✅ Upload successful! URL: {blob_url}")
            
            # Log to DB
            try:
                BlobLog.objects.create(
                    filename=filename,
                    url=blob_url,
                    file_size=file_size
                )
            except Exception as e:
                logger.error(f"⚠️ Failed to save BlobLog: {e}")

            return blob_url

        except Exception as e:
            logger.error(f"❌ Upload to Blob failed: {str(e)}", exc_info=True)
            return None

    def perform_create(self, serializer):
        model_file = self.request.data.get("model_file")
        
        # Si un fichier est fourni, on essaie de l'envoyer sur le Blob
        if model_file:
            blob_url = self._upload_to_blob(model_file)
            if blob_url:
                # Si succès, on enregistre l'URL du blob
                serializer.save(model_url=blob_url)
            else:
                # Si échec ou pas de token, on laisse le comportement par défaut (local)
                # Le modèle Geometry gère déjà l'assignation de model_url = file.url dans save()
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
