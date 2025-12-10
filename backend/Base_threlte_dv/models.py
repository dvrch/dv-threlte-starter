import random
import cloudinary  # Added import for cloudinary
from cloudinary_storage.storage import RawMediaCloudinaryStorage

from django.db import models

from .dv_config import TYPE_CHOICES


def get_default_position():
    return {"x": 0.0, "y": 0.0, "z": 0.0}


def get_default_rotation():
    return {"x": 0.0, "y": 0.0, "z": 0.0}


class Geometry(models.Model):
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="box")
    name = models.CharField(max_length=45, blank=True)

    # Champ pour gérer le téléversement de fichiers locaux
    model_file = models.FileField(
        upload_to="models/",
        blank=True,
        null=True,
        help_text="Fichier 3D local (.glb, .gltf)",
    )

    # Lien vers l'asset (Cloudinary ou B2)
    cloudinary_asset = models.ForeignKey(
        "CloudinaryAsset",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="geometries",
        help_text="Lien vers l'asset Cloudinary correspondant",
    )

    b2_asset = models.ForeignKey(
        "B2Asset",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="geometries",
        help_text="Lien vers l'asset B2 correspondant",
    )

    # Type de fichier 3D
    model_type = models.CharField(
        max_length=10,
        choices=[("gltf", "glTF"), ("glb", "GLB")],
        blank=True,
        help_text="Format du fichier 3D",
    )
    position = models.JSONField(default=get_default_position)
    rotation = models.JSONField(default=get_default_rotation)
    color = models.CharField(max_length=7, blank=True, default="#000000")  # Couleur

    def clean(self):
        if hasattr(self, "color") and self.color and not self.color.startswith("#"):
            self.color = "#" + self.color

    def format_position(self, x, y, z):
        self.position = {"x": x, "y": y, "z": z}

    def format_rotation(self, x, y, z):
        self.rotation = {"x": x, "y": y, "z": z}

    @property
    def current_asset(self):
        """Retourne l'asset actuel (B2 ou Cloudinary)"""
        return self.b2_asset or self.cloudinary_asset

    @property
    def asset_url(self):
        """Retourne l'URL de l'asset actuel"""
        asset = self.current_asset
        return asset.url if asset else None

    @property
    def asset_backend(self):
        """Retourne le backend de stockage actuel"""
        if self.b2_asset:
            return "b2"
        elif self.cloudinary_asset:
            return "cloudinary"
        return None

    def get_asset_info(self):
        """Retourne les informations complètes de l'asset"""
        asset = self.current_asset
        if not asset:
            return None

        info = {
            "backend": self.asset_backend,
            "url": asset.url,
            "file_name": getattr(asset, "file_name", None)
            or getattr(asset, "original_name", None),
            "file_size": getattr(asset, "file_size", None),
        }

        if hasattr(asset, "content_type"):
            info["content_type"] = asset.content_type
        if hasattr(asset, "format"):
            info["format"] = asset.format

        return info

    class Meta:
        ordering = ["-id"]  # Orden par défaut pour éviter les warnings de pagination


class BlobLog(models.Model):
    """
    Journal des fichiers uploadés sur Vercel Blob.
    Permet de garder une trace locale (en DB Neon) de ce qui est dans le Cloud.
    """

    filename = models.CharField(max_length=255)
    url = models.URLField(max_length=1024)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.PositiveIntegerField(
        null=True, blank=True, help_text="Taille en octets"
    )

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.filename} ({self.uploaded_at})"


class CloudinaryAsset(models.Model):
    asset_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Cloudinary Asset ID (unique, non-editable)",
    )
    public_id = models.CharField(
        max_length=255, unique=True, help_text="Cloudinary Public ID"
    )
    url = models.URLField(max_length=1024, help_text="URL de l'asset sur Cloudinary")
    asset_type = models.CharField(
        max_length=50, help_text="Type d'asset (image, video, raw, etc.)"
    )
    file_name = models.CharField(
        max_length=255, blank=True, null=True, help_text="Nom original du fichier"
    )
    format = models.CharField(
        max_length=50, blank=True, help_text="Format du fichier (ex: glb, png)"
    )
    file_size = models.PositiveIntegerField(
        null=True, blank=True, help_text="Taille du fichier en octets"
    )
    tags = models.JSONField(
        default=list, blank=True, help_text="Tags associés à l'asset"
    )
    metadata = models.JSONField(
        default=dict, blank=True, help_text="Métadonnées additionnelles de Cloudinary"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "Cloudinary Asset"
        verbose_name_plural = "Cloudinary Assets"

    def __str__(self):
        return self.file_name or self.public_id


class B2Asset(models.Model):
    """
    Modèle pour suivre les assets uploadés sur Backblaze B2.
    Remplace CloudinaryAsset pour le stockage B2.
    """

    b2_file_id = models.CharField(
        max_length=255, unique=True, help_text="ID unique du fichier sur B2"
    )
    file_name = models.CharField(
        max_length=255, help_text="Nom du fichier sur B2 (inclut le chemin)"
    )
    original_name = models.CharField(
        max_length=255, blank=True, null=True, help_text="Nom original du fichier"
    )
    url = models.URLField(
        max_length=1024, help_text="URL publique d'accès au fichier sur B2"
    )
    bucket_name = models.CharField(max_length=255, help_text="Nom du bucket B2")
    content_type = models.CharField(
        max_length=100, blank=True, help_text="Type MIME du fichier"
    )
    file_size = models.PositiveIntegerField(
        null=True, blank=True, help_text="Taille du fichier en octets"
    )
    checksum = models.CharField(
        max_length=64, blank=True, help_text="SHA256 ou MD5 du fichier"
    )
    upload_timestamp = models.DateTimeField(
        null=True, blank=True, help_text="Timestamp d'upload B2"
    )
    tags = models.JSONField(
        default=list, blank=True, help_text="Tags associés à l'asset"
    )
    metadata = models.JSONField(
        default=dict, blank=True, help_text="Métadonnées additionnelles"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "B2 Asset"
        verbose_name_plural = "B2 Assets"
        indexes = [
            models.Index(fields=["file_name"]),
            models.Index(fields=["bucket_name"]),
            models.Index(fields=["content_type"]),
        ]

    def __str__(self):
        return self.original_name or self.file_name

    @property
    def is_3d_model(self):
        """Vérifie si c'est un modèle 3D"""
        return self.content_type in [
            "model/gltf+json",
            "model/gltf-binary",
        ] or self.file_name.lower().endswith((".glb", ".gltf"))

    @property
    def is_image(self):
        """Vérifie si c'est une image"""
        return (
            self.content_type
            and self.content_type.startswith("image/")
            or self.file_name.lower().endswith(
                (".jpg", ".jpeg", ".png", ".gif", ".webp")
            )
        )
