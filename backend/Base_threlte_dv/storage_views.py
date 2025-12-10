from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .storage_manager import storage_manager
import json


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
