import os
import boto3
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import cloudinary
import cloudinary.uploader
from botocore.exceptions import NoCredentialsError, ClientError


class StorageManager:
    """Gestionnaire de stockage unifié pour B2, Cloudinary et Local"""

    def __init__(self):
        self.current_backend = self._detect_current_backend()

    def _detect_current_backend(self):
        """Détecte le backend de stockage actuel"""
        if getattr(settings, "USE_B2_STORAGE", False):
            return "b2"
        elif getattr(settings, "USE_CLOUDINARY", False):
            return "cloudinary"
        else:
            return "local"

    def get_storage_info(self):
        """Retourne les informations du stockage actuel"""
        info = {"backend": self.current_backend, "configured": True, "details": {}}

        if self.current_backend == "b2":
            info["details"] = {
                "bucket": getattr(settings, "AWS_STORAGE_BUCKET_NAME", None),
                "endpoint": getattr(settings, "AWS_S3_ENDPOINT_URL", None),
                "region": getattr(settings, "AWS_S3_REGION_NAME", None),
            }
            # Vérifier si les credentials sont présents
            if not all(
                [
                    getattr(settings, "AWS_ACCESS_KEY_ID", None),
                    getattr(settings, "AWS_SECRET_ACCESS_KEY", None),
                ]
            ):
                info["configured"] = False
                info["error"] = "B2 credentials manquantes"

        elif self.current_backend == "cloudinary":
            info["details"] = {
                "cloud_name": getattr(settings, "CLOUD_NAME", None),
                "api_base_url": getattr(settings, "CLOUDINARY_URL", None),
            }
            # Vérifier si Cloudinary est configuré
            if not all(
                [
                    getattr(settings, "CLOUD_NAME", None),
                    getattr(settings, "CLOUD_API_KEY", None),
                    getattr(settings, "CLOUD_API_SECRET", None),
                ]
            ):
                info["configured"] = False
                info["error"] = "Cloudinary credentials manquantes"
        else:
            info["details"] = {
                "media_root": getattr(settings, "MEDIA_ROOT", None),
                "media_url": getattr(settings, "MEDIA_URL", None),
            }

        return info

    def test_storage(self):
        """Teste le stockage actuel"""
        try:
            # Créer un fichier de test
            test_content = "Test de stockage - " + str(self.current_backend)
            test_filename = f"storage-test/{self.current_backend}-test.txt"

            # Sauvegarder le fichier
            file_path = default_storage.save(test_filename, ContentFile(test_content))

            # Vérifier l'URL
            file_url = default_storage.url(file_path)

            # Nettoyer
            if default_storage.exists(file_path):
                default_storage.delete(file_path)

            return {
                "success": True,
                "backend": self.current_backend,
                "test_file": file_path,
                "test_url": file_url,
                "message": f"Test {self.current_backend} réussi",
            }

        except Exception as e:
            return {
                "success": False,
                "backend": self.current_backend,
                "error": str(e),
                "message": f"Test {self.current_backend} échoué",
            }

    def list_available_backends(self):
        """Liste tous les backends disponibles avec leur statut"""
        backends = {
            "b2": {
                "name": "Backblaze B2",
                "available": bool(
                    os.environ.get("B2_KEY_ID") and os.environ.get("B2_APPLICATION_KEY")
                ),
                "current": self.current_backend == "b2",
            },
            "cloudinary": {
                "name": "Cloudinary",
                "available": bool(
                    os.environ.get("CLOUD_NAME") and os.environ.get("CLOUD_API_KEY")
                ),
                "current": self.current_backend == "cloudinary",
            },
            "local": {
                "name": "Stockage Local",
                "available": True,  # Toujours disponible
                "current": self.current_backend == "local",
            },
        }
        return backends

    def switch_backend(self, target_backend):
        """Bascule vers un autre backend (nécessite redémarrage)"""
        if target_backend not in ["b2", "cloudinary", "local"]:
            return {"success": False, "error": f"Backend {target_backend} non supporté"}

        backends = self.list_available_backends()
        if not backends[target_backend]["available"]:
            return {
                "success": False,
                "error": f"Backend {target_backend} non configuré",
            }

        # Retourne les variables d'environnement à définir
        env_config = {
            "b2": {"USE_B2_STORAGE": "True", "USE_CLOUDINARY": "False"},
            "cloudinary": {"USE_B2_STORAGE": "False", "USE_CLOUDINARY": "True"},
            "local": {"USE_B2_STORAGE": "False", "USE_CLOUDINARY": "False"},
        }

        return {
            "success": True,
            "message": f"Définissez ces variables d'environnement sur Railway:",
            "backend": target_backend,
            "env_vars": env_config[target_backend],
            "restart_required": True,
        }


# Instance globale du gestionnaire
storage_manager = StorageManager()
