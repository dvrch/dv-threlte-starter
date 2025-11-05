from django.db import migrations

def populate_model_urls(apps, schema_editor):
    Geometry = apps.get_model('Base_threlte_dv', 'Geometry')
    
    type_to_url = {
        'sphere': '/src/routes/sphere/+page.svelte',
        'vague': '/src/routes/vague/+page.svelte',
        'tissus': '/src/routes/bibi/tissus-simulat.svelte',
        'desk': '/src/routes/desksc/+page.svelte',
        'nissan': '/src/routes/Spaceship/Nissan.svelte',
        'bibi': '/src/routes/bibi/bibanime.svelte',
        'garden': '/src/routes/app/models/garden.svelte',
        'nissangame': '/src/routes/app/nissangame.svelte',
        'bibigame': '/src/routes/app/bibigame.svelte',
    }

    for geometry in Geometry.objects.all():
        if geometry.type in type_to_url:
            geometry.model_url = type_to_url[geometry.type]
            geometry.model_type = 'from_file'
            geometry.save()

class Migration(migrations.Migration):

    dependencies = [
        ('Base_threlte_dv', '0002_alter_geometry_options_geometry_model_type_and_more'),
    ]

    operations = [
        migrations.RunPython(populate_model_urls),
    ]