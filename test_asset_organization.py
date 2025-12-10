#!/usr/bin/env python3
"""
Test script to verify asset organization before B2 upload
"""

import os
from pathlib import Path


def check_assets():
    """Vérifie que tous les assets requis sont présents"""

    base_dir = Path(__file__).parent
    static_dir = base_dir / "static"

    # Assets attendus d'après la configuration
    expected_models = [
        "ghost.glb",
        "garden.glb",
        "spaceship.glb",
        "DcYcU.glb",
        "threlte.glb",
        "character.glb",
        "mob1.glb",
        "mob2.glb",
        "world.glb",
        "world0.glb",
        "world1.glb",
        "world2.glb",
        "mario.glb",
        "bibi.glb",
        "bibi3.glb",
        "cloth_sim.glb",
    ]

    expected_textures = [
        "star.png",
        "energy-beam-opacity.png",
        "sky.jpg",
        "mario.png",
        "bibi.png",
        "diamond.jpg",
    ]

    print("🔍 Vérification des assets...\n")

    # Vérifier les modèles
    models_dir = static_dir / "models"
    missing_models = []
    found_models = []

    for model in expected_models:
        model_path = models_dir / model
        if model_path.exists():
            size = model_path.stat().st_size
            found_models.append((model, size))
        else:
            missing_models.append(model)

    # Vérifier les textures
    textures_dir = static_dir / "textures"
    missing_textures = []
    found_textures = []

    for texture in expected_textures:
        texture_path = textures_dir / texture
        if texture_path.exists():
            size = texture_path.stat().st_size
            found_textures.append((texture, size))
        else:
            missing_textures.append(texture)

    # Afficher les résultats
    print(f"📦 Modèles 3D: {len(found_models)}/{len(expected_models)} trouvés")
    for model, size in found_models:
        print(f"  ✅ {model} ({size:,} bytes)")

    if missing_models:
        print(f"  ❌ Manquants: {', '.join(missing_models)}")

    print(f"\n🎨 Textures: {len(found_textures)}/{len(expected_textures)} trouvées")
    for texture, size in found_textures:
        print(f"  ✅ {texture} ({size:,} bytes)")

    if missing_textures:
        print(f"  ❌ Manquantes: {', '.join(missing_textures)}")

    # Vérifier les autres fichiers dans les dossiers
    all_models = list(models_dir.glob("*.glb")) + list(models_dir.glob("*.gltf"))
    all_textures = list(textures_dir.glob("*.png")) + list(textures_dir.glob("*.jpg"))

    print(f"\n📊 Total:")
    print(f"  - Modèles dans le dossier: {len(all_models)}")
    print(f"  - Textures dans le dossier: {len(all_textures)}")

    # Vérifier si tous les assets requis sont présents
    all_present = len(missing_models) == 0 and len(missing_textures) == 0

    if all_present:
        print("\n🎉 Tous les assets requis sont présents!")
        print("💡 Prochaine étape: Configurez les credentials B2 et lancez l'upload")
    else:
        print("\n⚠️  Certains assets manquent. Veuillez les ajouter avant l'upload.")

    return all_present


if __name__ == "__main__":
    check_assets()
