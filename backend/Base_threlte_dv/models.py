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
        is_new = self.pk is None
        
        # Store original model_file to check if it changed
        original_model_file_url = ""
        if not is_new:
            try:
                original_model_file_url = Geometry.objects.get(pk=self.pk).model_file.url
            except Geometry.DoesNotExist:
                pass # Object might have been deleted and recreated quickly

        super().save(*args, **kwargs) # This triggers Cloudinary upload if model_file is set

        # If model_file was provided and it resulted in a valid Cloudinary URL
        if self.model_file and self.model_file.url and self.model_file.url.startswith('https://res.cloudinary.com/'):
            # Ensure model_url is updated to the Cloudinary URL
            if self.model_url != self.model_file.url:
                self.model_url = self.model_file.url
                # Save again only if model_url actually changed to avoid infinite loop
                super().save(update_fields=["model_url"])

            # Use the admin API to get full resource details
            try:
                public_id_with_folder = '/'.join(self.model_file.url.split('/')[-2:])
                public_id = public_id_with_folder.split('.')[0]
                
                resource_details = cloudinary.api.resource(public_id, resource_type="raw")
                
                if resource_details:
                    CloudinaryAsset.objects.update_or_create(
                        public_id=resource_details.get("public_id"),
                        defaults={
                            'asset_id': resource_details.get("asset_id"),
                            'url': resource_details.get("secure_url"),
                            'asset_type': resource_details.get("resource_type"),
                            'file_name': self.model_file.name,
                            'format': resource_details.get("format"),
                            'file_size': resource_details.get("bytes"),
                            'tags': resource_details.get("tags", []),
                            'metadata': resource_details.get("metadata", {}),
                        }
                    )
            except Exception as e:
                print(f"Error fetching full resource details from Cloudinary for Geometry {self.pk}: {e}")

        elif self.model_file and not self.model_file.url.startswith('https://res.cloudinary.com/'):
            # This case means a file was provided but Cloudinary upload likely failed or returned a local path
            print(f"Warning: model_file provided for Geometry {self.pk} but did not result in a Cloudinary URL: {self.model_file.url}")
            # Clear model_url if Cloudinary upload failed
            if self.model_url:
                self.model_url = ""
                super().save(update_fields=["model_url"])
        elif not self.model_file and self.model_url:
            # If model_file is cleared but model_url still exists, clear CloudinaryAsset and model_url
            try:
                parsed_url = cloudinary.CloudinaryImage(self.model_url)
                public_id = parsed_url.public_id
                if public_id:
                    CloudinaryAsset.objects.filter(public_id=public_id).delete()
            except Exception as e:
                print(f"Error cleaning up CloudinaryAsset for Geometry {self.pk}: {e}")
            
            self.model_url = ""
            super().save(update_fields=["model_url"])


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
