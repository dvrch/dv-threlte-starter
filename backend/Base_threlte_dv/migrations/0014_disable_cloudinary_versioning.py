"""Fix Cloudinary upload options to disable versioning"""

from django.db import migrations


def update_cloudinary_settings(apps, schema_editor):
    """Update serializer to use overwrite=True and disable versioning"""
    # This is a simple migration - the actual fix is in the serializer code
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("Base_threlte_dv", "0012_geometry_scale"),
    ]

    operations = [
        migrations.RunPython(
            update_cloudinary_settings, reverse_code=migrations.RunPython.noop
        ),
    ]
