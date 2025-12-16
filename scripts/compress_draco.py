#!/usr/bin/env python3
import subprocess
import os
import sys
from pathlib import Path

def compress_with_gltf_transform(input_path, output_path=None):
    """Compresse un fichier GLB avec gltf-transform (Node.js)"""
    if output_path is None:
        output_path = input_path.replace('.glb', '_draco.glb')
    
    cmd = [
        'npx', 'gltf-transform', 'draco',
        input_path,
        output_path
    ]
    
    try:
        print(f"🔄 Compression de {input_path}...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Fichier compressé : {output_path}")
            original_size = os.path.getsize(input_path)
            compressed_size = os.path.getsize(output_path)
            compression_ratio = (1 - compressed_size/original_size) * 100
            
            print(f"📊 Taille originale : {original_size/1024/1024:.2f} MB")
            print(f"📊 Taille compressée : {compressed_size/1024/1024:.2f} MB")
            print(f"📈 Ratio de compression : {compression_ratio:.1f}%")
            
            return output_path
        else:
            print(f"❌ Erreur : {result.stderr}")
            return None
    except FileNotFoundError:
        print("❌ gltf-transform n'est pas installé. Installez-le avec :")
        print("   npm install -g @gltf-transform/cli")
        return None

def batch_compress(folder_path):
    """Compresse tous les GLB dans un dossier"""
    folder = Path(folder_path)
    glb_files = list(folder.glob('*.glb'))
    
    print(f"📁 Dossier : {folder}")
    print(f"📦 {len(glb_files)} fichiers GLB trouvés")
    
    for glb_file in glb_files:
        # Ne pas recompresser les fichiers déjà compressés
        if '_draco' not in glb_file.stem:
            output_file = glb_file.parent / f"{glb_file.stem}_draco.glb"
            compress_with_gltf_transform(str(glb_file), str(output_file))
            print("-" * 50)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Compression d'un fichier spécifique
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        compress_with_gltf_transform(input_file, output_file)
    else:
        # Compression en batch
        folder = input("Entrez le chemin du dossier (défaut: ./static/public/) : ")
        folder = folder.strip() if folder else "./static/public/"
        batch_compress(folder)
