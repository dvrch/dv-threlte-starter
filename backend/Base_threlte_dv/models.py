from django.db import models
from .dv_config import TYPE_CHOICES
import random

def get_default_position():
    return {"x": 0.0, "y": 0.0, "z": 0.0}

def get_default_rotation():
    return {"x": 0.0, "y": 0.0, "z": 0.0}

class Geometry(models.Model):
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, 
                          default='box')
    name = models.CharField(max_length=45, blank=True)
    
    # Champ pour gérer le téléversement de fichiers locaux
    model_file = models.FileField(
        upload_to='models/', 
        blank=True, 
        null=True, 
        help_text="Fichier 3D local (.glb, .gltf)"
    )
    
    # URL du modèle 3D (sera rempli automatiquement)
    model_url = models.URLField(max_length=1024, blank=True, 
                              help_text="URL du fichier 3D (rempli automatiquement depuis model_file)")
    
    # Type de fichier 3D
    model_type = models.CharField(max_length=10, choices=[
        ('gltf', 'glTF'),
        ('glb', 'GLB')
    ], blank=True, help_text="Format du fichier 3D")
    position = models.JSONField(default=get_default_position)
    rotation = models.JSONField(default=get_default_rotation)
    color = models.CharField(max_length=7, blank=True, default='#000000')  # Couleur

    def get_random_color():
        return Geometry.color
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.model_file and self.model_url != self.model_file.url:
            self.model_url = self.model_file.url
            super().save(update_fields=['model_url'])

    def clean(self):
        if hasattr(self, 'color') and self.color and not self.color.startswith('#'):
            self.color = '#' + self.color    

    def format_position(self, x, y, z):
        self.position = {"x": x, "y": y, "z": z}

    def format_rotation(self, x, y, z):
        self.rotation = {"x": x, "y": y, "z": z}

    class Meta:
        ordering = ['-id']  # Orden par défaut pour éviter les warnings de pagination