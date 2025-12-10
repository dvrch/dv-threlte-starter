#!/usr/bin/env python3
"""
Script simple pour mettre à jour les références d'assets dans le code Svelte
"""

import os
import re
from pathlib import Path


def update_svelte_files():
    """Met à jour les fichiers Svelte pour utiliser les URLs B2"""

    # Mapping des fichiers locaux vers les URLs B2 (à remplir après upload)
    # Pour l'instant, utilisons un exemple de structure
    b2_base_url = "https://f001.backblazeb2.com/file/43dvcapp/"

    # Mapping des modèles connus
    asset_mappings = {
        "/models/ghost.glb": f"{b2_base_url}models/ghost.glb",
        "/models/garden.glb": f"{b2_base_url}models/garden.glb",
        "/models/spaceship.glb": f"{b2_base_url}models/spaceship.glb",
        "/models/DcYcU.glb": f"{b2_base_url}models/DcYcU.glb",
        "/models/threlte.glb": f"{b2_base_url}models/threlte.glb",
        "/models/scene.gltf": f"{b2_base_url}models/scene.gltf",
        "/textures/star.png": f"{b2_base_url}textures/star.png",
        "/textures/energy-beam-opacity.png": f"{b2_base_url}textures/energy-beam-opacity.png",
    }

    # Fichiers à mettre à jour
    svelte_files = [
        "src/lib/components/models/ghost.svelte",
        "src/lib/components/models/garden.svelte",
        "src/lib/components/models/spaceship.svelte",
        "src/lib/components/models/DcYcU.svelte",
        "src/lib/components/models/threlte.svelte",
        "src/routes/app/models/garden.svelte",
        "src/routes/Spaceship/models/spaceship.svelte",
        "src/routes/Spaceship/models/ghost.svelte",
        "src/routes/planet/Earth.svelte",
        "src/lib/components/Stars.svelte",
        "src/routes/Spaceship/Stars.svelte",
        "src/routes/Spaceship/models/spaceship.svelte",
    ]

    project_root = Path("/home/kd/Bureau/dv-threlte-starter")
    updated_files = []

    for file_path in svelte_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"Mise à jour de {file_path}")

            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()

                original_content = content

                # Remplacer les références useGltf
                for local_path, b2_url in asset_mappings.items():
                    # Patterns différents pour useGltf
                    patterns = [
                        f"useGltf('{local_path}')",
                        f'useGltf("{local_path}")',
                        f"useGltf('{b2_base_url}{local_path[1:]}')",  # Si déjà partiellement migré
                        f'useGltf("{b2_base_url}{local_path[1:]}")',
                    ]

                    for pattern in patterns:
                        content = content.replace(pattern, f"useGltf('{b2_url}')")

                # Remplacer les références useTexture
                for local_path, b2_url in asset_mappings.items():
                    if "texture" in local_path or local_path.endswith(
                        (".png", ".jpg", ".jpeg", ".webp")
                    ):
                        patterns = [
                            f"useTexture('{local_path}')",
                            f'useTexture("{local_path}")',
                        ]

                        for pattern in patterns:
                            content = content.replace(
                                pattern, f"useTexture('{b2_url}')"
                            )

                # Sauvegarder si modifié
                if content != original_content:
                    with open(full_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    updated_files.append(file_path)
                    print(f"  ✅ Mis à jour")
                else:
                    print(f"  ⏭️  Aucune modification nécessaire")

            except Exception as e:
                print(f"  ❌ Erreur: {e}")
        else:
            print(f"⚠️  Fichier non trouvé: {file_path}")

    return updated_files


def update_js_files():
    """Met à jour les fichiers JavaScript qui référencent des assets"""

    b2_base_url = "https://f001.backblazeb2.com/file/43dvcapp/"

    # Mapping pour les fichiers JS
    asset_mappings = {
        "garden.glb": f"{b2_base_url}models/garden.glb",
        "character.glb": f"{b2_base_url}models/character.glb",
        "mob1.glb": f"{b2_base_url}models/mob1.glb",
        "mob2.glb": f"{b2_base_url}models/mob2.glb",
        "world.glb": f"{b2_base_url}models/world.glb",
        "world0.glb": f"{b2_base_url}models/world0.glb",
        "world1.glb": f"{b2_base_url}models/world1.glb",
        "world2.glb": f"{b2_base_url}models/world2.glb",
        "sky.jpg": f"{b2_base_url}textures/sky.jpg",
        "mario.glb": f"{b2_base_url}models/mario.glb",
        "mario.png": f"{b2_base_url}textures/mario.png",
        "diamond.jpg": f"{b2_base_url}textures/diamond.jpg",
        "bibi.glb": f"{b2_base_url}models/bibi.glb",
        "bibi3.glb": f"{b2_base_url}models/bibi3.glb",
        "bibi.png": f"{b2_base_url}textures/bibi.png",
        "cloth_sim.glb": f"{b2_base_url}models/cloth_sim.glb",
    }

    # Fichiers JS à mettre à jour
    js_files = [
        "src/routes/app/+page.server.js",
        "src/routes/fkisios-main/src/tool/loader.js",
        "src/routes/fkisios-main/src/shader/rubis.js",
        "src/routes/fkisios-main/src/engine/graphic.js",
        "src/routes/fkisios-main/step_00/app.js",
        "src/routes/fkisios-main/step_01/app.js",
        "src/routes/fkisios-main/step_02/app.js",
        "src/routes/fkisios-main/step_03/app.js",
        "src/routes/fkisios-main/step_04/app.js",
        "src/routes/fkisios-main/step_05/app.js",
        "src/routes/fkisios-main/step_06/app.svelte",
        "src/routes/bibi/demo_03.ts",
        "src/routes/bibi/demo_04.ts",
        "src/routes/bibi/demo_06.ts",
        "src/routes/bibi/demo_08.ts",
        "src/routes/bibi/demo_09.ts",
    ]

    project_root = Path("/home/kd/Bureau/dv-threlte-starter")
    updated_files = []

    for file_path in js_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"Mise à jour de {file_path}")

            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()

                original_content = content

                # Remplacer les références de fichiers
                for filename, b2_url in asset_mappings.items():
                    # Patterns pour les chargements de fichiers
                    patterns = [
                        f"'{filename}'",
                        f'"{filename}"',
                        f"'./{filename}'",
                        f'"./{filename}"',
                        f"'../{filename}'",
                        f'"../{filename}"',
                        f"'/static/{filename}'",
                        f'"/static/{filename}"',
                    ]

                    for pattern in patterns:
                        content = content.replace(pattern, f"'{b2_url}'")

                # Sauvegarder si modifié
                if content != original_content:
                    with open(full_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    updated_files.append(file_path)
                    print(f"  ✅ Mis à jour")
                else:
                    print(f"  ⏭️  Aucune modification nécessaire")

            except Exception as e:
                print(f"  ❌ Erreur: {e}")
        else:
            print(f"⚠️  Fichier non trouvé: {file_path}")

    return updated_files


def create_b2_url_config():
    """Crée un fichier de configuration pour les URLs B2"""

    config_content = """// Configuration des URLs Backblaze B2 pour les assets
export const B2_BASE_URL = 'https://f001.backblazeb2.com/file/43dvcapp/';

// Mapping des assets vers leurs URLs B2
export const B2_ASSETS = {
  // Modèles 3D
  'ghost.glb': \`\${B2_BASE_URL}models/ghost.glb\`,
  'garden.glb': \`\${B2_BASE_URL}models/garden.glb\`,
  'spaceship.glb': \`\${B2_BASE_URL}models/spaceship.glb\`,
  'DcYcU.glb': \`\${B2_BASE_URL}models/DcYcU.glb\`,
  'threlte.glb': \`\${B2_BASE_URL}models/threlte.glb\`,
  'scene.gltf': \`\${B2_BASE_URL}models/scene.gltf\`,
  'character.glb': \`\${B2_BASE_URL}models/character.glb\`,
  'mob1.glb': \`\${B2_BASE_URL}models/mob1.glb\`,
  'mob2.glb': \`\${B2_BASE_URL}models/mob2.glb\`,
  'world.glb': \`\${B2_BASE_URL}models/world.glb\`,
  'world0.glb': \`\${B2_BASE_URL}models/world0.glb\`,
  'world1.glb': \`\${B2_BASE_URL}models/world1.glb\`,
  'world2.glb': \`\${B2_BASE_URL}models/world2.glb\`,
  'mario.glb': \`\${B2_BASE_URL}models/mario.glb\`,
  'bibi.glb': \`\${B2_BASE_URL}models/bibi.glb\`,
  'bibi3.glb': \`\${B2_BASE_URL}models/bibi3.glb\`,
  'cloth_sim.glb': \`\${B2_BASE_URL}models/cloth_sim.glb\`,
  
  // Textures
  'star.png': \`\${B2_BASE_URL}textures/star.png\`,
  'energy-beam-opacity.png': \`\${B2_BASE_URL}textures/energy-beam-opacity.png\`,
  'sky.jpg': \`\${B2_BASE_URL}textures/sky.jpg\`,
  'mario.png': \`\${B2_BASE_URL}textures/mario.png\`,
  'bibi.png': \`\${B2_BASE_URL}textures/bibi.png\`,
  'diamond.jpg': \`\${B2_BASE_URL}textures/diamond.jpg\`,
};

// Fonction utilitaire pour obtenir l'URL B2 d'un asset
export function getB2AssetUrl(assetName: string): string {
  return B2_ASSETS[assetName] || \`\${B2_BASE_URL}assets/\${assetName}\`;
}
"""

    config_path = Path("/home/kd/Bureau/dv-threlte-starter/src/lib/config/b2-assets.ts")

    try:
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(config_content)
        print(f"✅ Configuration B2 créée: {config_path}")
        return True
    except Exception as e:
        print(f"❌ Erreur création configuration: {e}")
        return False


def main():
    """Fonction principale"""
    print("🔄 Mise à jour des références d'assets pour Backblaze B2...")

    # Créer la configuration B2
    print("\n📝 Création de la configuration B2...")
    create_b2_url_config()

    # Mettre à jour les fichiers Svelte
    print("\n🔧 Mise à jour des fichiers Svelte...")
    svelte_updated = update_svelte_files()

    # Mettre à jour les fichiers JS
    print("\n🔧 Mise à jour des fichiers JavaScript...")
    js_updated = update_js_files()

    # Résumé
    print(f"\n📊 Résumé:")
    print(f"  ✅ Fichiers Svelte mis à jour: {len(svelte_updated)}")
    print(f"  ✅ Fichiers JS mis à jour: {len(js_updated)}")

    if svelte_updated or js_updated:
        print(f"\n🎉 Mise à jour terminée!")
        print(f"\n📝 Prochaines étapes:")
        print(f"  1. Uploader les assets vers Backblaze B2")
        print(f"  2. Vérifier que les URLs sont correctes")
        print(f"  3. Tester l'application")
    else:
        print(f"\n⚠️  Aucun fichier mis à jour")


if __name__ == "__main__":
    main()
