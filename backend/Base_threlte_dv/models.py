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

    model_url = models.URLField(
        max_length=1024,
        blank=True,
        null=True,
        help_text="URL du modèle 3D sur Cloudinary",
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
        if self.color and not str(self.color).startswith("#"):
            self.color = "#" + str(self.color)

    def format_position(self, x, y, z):
        self.position = {"x": x, "y": y, "z": z}

    def format_rotation(self, x, y, z):
        self.rotation = {"x": x, "y": y, "z": z}

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
        return str(self.file_name or self.public_id)
