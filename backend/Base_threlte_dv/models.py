import random
import cloudinary # Added import for cloudinary
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
        storage=RawMediaCloudinaryStorage(),
    )

    # URL du modèle 3D (sera rempli automatiquement)
    model_url = models.URLField(
        max_length=1024,
        blank=True,
        help_text="URL du fichier 3D (rempli automatiquement depuis model_file)",
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

    def save(self, *args, **kwargs):
        # First, save the instance to handle the file upload via RawMediaCloudinaryStorage.
        # The `super().save()` call will trigger the upload and populate `self.model_file`
        # with Cloudinary details like .url and .public_id.
        super().save(*args, **kwargs)

        # After the save, check if a file was uploaded to Cloudinary.
        # We can verify this by checking for the `public_id` attribute, which is added
        # by the cloudinary_storage backend.
        if self.model_file and hasattr(self.model_file, 'public_id'):
            
            # The URL from the storage is the source of truth.
            correct_url = self.model_file.url
            
            # Update the Geometry instance's own model_url field if it's not correct.
            if self.model_url != correct_url:
                self.model_url = correct_url
                # Save again, but only update this one field to prevent an infinite loop.
                super().save(update_fields=['model_url'])

            # Now, create or update our asset tracking table with the correct info.
            # This logic no longer makes a second API call. It trusts the upload result.
            CloudinaryAsset.objects.update_or_create(
                public_id=self.model_file.public_id,
                defaults={
                    'asset_id': getattr(self.model_file, 'asset_id', None),
                    'url': correct_url,
                    'asset_type': 'raw',  # We know it's 'raw' because we use RawMediaCloudinaryStorage
                    'file_name': self.model_file.name,
                    'file_size': self.model_file.size,
                }
            )
        
        # This part handles the case where the model_file is cleared in the admin.
        elif not self.model_file and self.model_url:
            # If the file is removed, we should also clear our local URL.
            self.model_url = ""
            super().save(update_fields=['model_url'])
            # A more advanced implementation could also delete the CloudinaryAsset entry
            # or the file on Cloudinary, but that can be dangerous. For now, we just clear the URL.


    def clean(self):
        if hasattr(self, "color") and self.color and not self.color.startswith("#"):
            self.color = "#" + self.color

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
    file_size = models.PositiveIntegerField(null=True, blank=True, help_text="Taille en octets")
    
    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.filename} ({self.uploaded_at})"


class CloudinaryAsset(models.Model):
    asset_id = models.CharField(max_length=255, blank=True, null=True, help_text="Cloudinary Asset ID (unique, non-editable)")
    public_id = models.CharField(max_length=255, unique=True, help_text="Cloudinary Public ID")
    url = models.URLField(max_length=1024, help_text="URL de l'asset sur Cloudinary")
    asset_type = models.CharField(max_length=50, help_text="Type d'asset (image, video, raw, etc.)")
    file_name = models.CharField(max_length=255, blank=True, null=True, help_text="Nom original du fichier")
    format = models.CharField(max_length=50, blank=True, help_text="Format du fichier (ex: glb, png)")
    file_size = models.PositiveIntegerField(null=True, blank=True, help_text="Taille du fichier en octets")
    tags = models.JSONField(default=list, blank=True, help_text="Tags associés à l'asset")
    metadata = models.JSONField(default=dict, blank=True, help_text="Métadonnées additionnelles de Cloudinary")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "Cloudinary Asset"
        verbose_name_plural = "Cloudinary Assets"

    def __str__(self):
        return self.file_name or self.public_id
