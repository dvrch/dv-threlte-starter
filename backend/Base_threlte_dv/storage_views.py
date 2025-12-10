from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .storage_manager import storage_manager
from .models import B2Asset
import json
import requests
import os
import uuid
from datetime import datetime


@api_view(["GET"])
@permission_classes([AllowAny])
def storage_info(request):
    """API pour obtenir les informations du stockage actuel"""
    try:
        info = storage_manager.get_storage_info()
        return Response(info, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {
                "error": str(e),
                "message": "Erreur lors de la récupération des infos de stockage",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def storage_backends(request):
    """API pour lister tous les backends disponibles"""
    try:
        backends = storage_manager.list_available_backends()
        return Response(backends, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": str(e), "message": "Erreur lors de la liste des backends"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def storage_switch(request):
    """API pour basculer de backend de stockage"""
    try:
        data = json.loads(request.body) if request.body else {}
        target_backend = data.get("backend")

        if not target_backend:
            return Response(
                {
                    "error": "backend requis",
                    "message": "Veuillez spécifier un backend (b2, cloudinary, local)",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = storage_manager.switch_backend(target_backend)

        if result["success"]:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

    except json.JSONDecodeError:
        return Response(
            {
                "error": "JSON invalide",
                "message": "Le corps de la requête doit être du JSON valide",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        return Response(
            {"error": str(e), "message": "Erreur lors du basculement de backend"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def storage_test(request):
    """API pour tester le stockage actuel"""
    try:
        result = storage_manager.test_storage()

        if result["success"]:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        return Response(
            {"error": str(e), "message": "Erreur lors du test de stockage"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def storage_status(request):
    """API pour obtenir un statut complet du système de stockage"""
    try:
        # Récupérer les informations actuelles
        current_info = storage_manager.get_storage_info()
        available_backends = storage_manager.list_available_backends()

        # Tester le stockage actuel
        test_result = storage_manager.test_storage()

        # Combiner toutes les informations
        status_data = {
            "current": current_info,
            "available": available_backends,
            "test": test_result,
            "summary": {
                "backend": current_info["backend"],
                "configured": current_info["configured"],
                "working": test_result["success"],
                "available_count": sum(
                    1 for b in available_backends.values() if b["available"]
                ),
            },
        }

        return Response(status_data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": str(e), "message": "Erreur lors de la récupération du statut"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def b2_asset_proxy(request, asset_name):
    """API endpoint pour servir les assets B2 avec autorisation"""
    try:
        # Pour l'instant, utiliser une approche simple avec l'URL B2 directe
        # Plus tard, nous pourrons ajouter l'autorisation B2 si nécessaire
        b2_base_url = "https://f003.backblazeb2.com/file/43dvcapp/"
        asset_url = f"{b2_base_url}{asset_name}"

        # Récupérer le fichier depuis B2
        response = requests.get(asset_url, stream=True)

        if response.status_code == 200:
            # Créer une réponse HTTP avec le contenu du fichier
            django_response = HttpResponse(
                response.content,
                content_type=response.headers.get(
                    "content-type", "application/octet-stream"
                ),
            )

            # Ajouter les headers CORS pour permettre l'accès depuis le frontend
            django_response["Access-Control-Allow-Origin"] = "*"
            django_response["Access-Control-Allow-Methods"] = "GET"
            django_response["Access-Control-Allow-Headers"] = "Content-Type"

            # Ajouter les headers de cache si présents
            if "cache-control" in response.headers:
                django_response["Cache-Control"] = response.headers["cache-control"]
            if "etag" in response.headers:
                django_response["ETag"] = response.headers["etag"]

            return django_response
        else:
            return Response(
                {"error": f"B2 asset not found: {asset_name}"},
                status=status.HTTP_404_NOT_FOUND,
            )

    except requests.exceptions.RequestException as e:
        return Response(
            {"error": f"Failed to fetch from B2: {str(e)}"},
            status=status.HTTP_502_BAD_GATEWAY,
        )
    except Exception as e:
        return Response(
            {
                "error": str(e),
                "message": "Erreur lors de la récupération de l'asset B2",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
@csrf_exempt
def b2_upload(request):
    """API endpoint pour uploader des fichiers vers B2"""
    try:
        if "file" not in request.FILES:
            return Response(
                {"error": "No file provided", "message": "Veuillez fournir un fichier"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        file = request.FILES["file"]

        # Validation du fichier
        if not file.name.endswith((".glb", ".gltf", ".png", ".jpg", ".jpeg", ".webp")):
            return Response(
                {
                    "error": "Invalid file type",
                    "message": "Format de fichier non supporté",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Utiliser le storage manager pour uploader
        result = storage_manager.upload_file(file, file.name)

        if result["success"]:
            # Créer une entrée B2Asset dans la base de données
            b2_asset = B2Asset.objects.create(
                b2_file_id=result.get("file_id", str(uuid.uuid4())),
                file_name=result["file_name"],
                original_name=file.name,
                url=result["url"],
                bucket_name=result.get("bucket_name", "43dvcapp"),
                content_type=file.content_type or "application/octet-stream",
                file_size=file.size,
                upload_timestamp=datetime.now(),
            )

            return Response(
                {
                    "success": True,
                    "message": "Fichier uploadé avec succès",
                    "file": {
                        "id": b2_asset.id,
                        "name": b2_asset.original_name,
                        "url": b2_asset.url,
                        "size": b2_asset.file_size,
                        "content_type": b2_asset.content_type,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {
                    "error": "Upload failed",
                    "message": result.get("error", "Erreur lors de l'upload"),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    except Exception as e:
        return Response(
            {"error": str(e), "message": "Erreur lors de l'upload vers B2"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
