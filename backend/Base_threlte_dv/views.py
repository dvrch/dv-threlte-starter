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
    """
    def post(self, request):
        filename = request.data.get('filename')
        if not filename:
            return Response({"error": "A 'filename' must be provided."}, status=status.HTTP_400_BAD_REQUEST)

        token = os.environ.get('BLOB_READ_WRITE_TOKEN')
        if not token:
            # In production, you'd want to log this error.
            print("CRITICAL: BLOB_READ_WRITE_TOKEN is not set.")
            return Response({"error": "Server is not configured for file uploads."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        headers = {
            'Authorization': f'Bearer {token}',
        }
        
        # The Vercel Blob API endpoint for creating a new blob and getting a presigned URL
        api_url = f'https://blob.vercel-storage.com?pathname={filename}'

        try:
            response = requests.post(api_url, headers=headers, json={})
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            
            blob_data = response.json()
            return Response(blob_data)

        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Vercel Blob API: {e}")
            # Optionally, inspect response if available: print(e.response.text)
            return Response({"error": "Failed to communicate with the blob storage service."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
