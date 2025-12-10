"""
Vue Django pour servir les assets B2 de manière sécurisée
"""

import os
import boto3
from botocore.exceptions import ClientError
from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.http import condition
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response


def get_b2_client():
    """Crée un client B2 avec les credentials"""
    return boto3.client(
        "s3",
        endpoint_url=os.environ.get("B2_ENDPOINT_URL"),
        aws_access_key_id=os.environ.get("B2_KEY_ID"),
        aws_secret_access_key=os.environ.get("B2_APPLICATION_KEY"),
        region_name=os.environ.get("B2_REGION", "us-west-003"),
    )


@csrf_exempt
@api_view(["GET"])
def serve_b2_asset(request, asset_name):
    """
    Sert un asset depuis B2 bucket privé de manière sécurisée
    URL: /api/assets/b2/{asset_name}
    """
    try:
        # Liste des assets autorisés (sécurité)
        allowed_assets = [
            "bibi.png",
            "cloth_sim.glb",
            "bibi.glb",
            "mario.glb",
            "peagh-drap.glb",
            "DRAP+Barrel Model1.glb",
            "lebowski.png",
        ]

        if asset_name not in allowed_assets:
            return JsonResponse({"error": "Asset not found"}, status=404)

        # Connexion à B2
        s3_client = get_b2_client()
        bucket_name = os.environ.get("B2_BUCKET_NAME", "43dvcapp")

        try:
            # Récupérer le fichier depuis B2
            response = s3_client.get_object(Bucket=bucket_name, Key=asset_name)

            # Préparer la réponse HTTP
            content_type = response.get("ContentType", "application/octet-stream")
            file_content = response["Body"].read()

            # Créer la réponse avec les headers appropriés
            http_response = HttpResponse(file_content, content_type=content_type)

            # Headers pour le cache et CORS (important pour Vercel)
            http_response["Cache-Control"] = "public, max-age=3600"  # 1 heure
            http_response["Access-Control-Allow-Origin"] = "*"  # CORS pour Vercel
            http_response["Access-Control-Allow-Methods"] = "GET"
            http_response["Access-Control-Allow-Headers"] = "*"

            return http_response

        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                raise Http404("Asset not found")
            return JsonResponse({"error": f"B2 error: {str(e)}"}, status=500)

    except Exception as e:
        return JsonResponse({"error": f"Server error: {str(e)}"}, status=500)


@csrf_exempt
@api_view(["GET"])
def list_available_assets(request):
    """
    Liste tous les assets disponibles (pour le frontend)
    URL: /api/assets/list
    """
    try:
        from backend.Base_threlte_dv.models import B2Asset

        assets = B2Asset.objects.all()
        asset_list = []

        for asset in assets:
            asset_list.append(
                {
                    "name": asset.file_name,
                    "url": f"/api/assets/b2/{asset.file_name}",
                    "size": asset.file_size,
                    "type": asset.content_type,
                }
            )

        return Response(
            {
                "success": True,
                "assets": asset_list,
                "base_url": f"{os.environ.get('PUBLIC_API_URL', 'http://localhost:8000')}/api/assets/b2/",
            }
        )

    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)
