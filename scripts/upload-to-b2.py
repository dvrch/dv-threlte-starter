"""
📤 Script d'upload vers Backblaze B2
Utilise les fichiers téléchargés depuis Vercel Blob (vercel-blob-backup/)
et les uploade vers Backblaze B2.

Prérequis:
    pip install boto3

Usage:
    python scripts/upload-to-b2.py
"""

import os
import json
from pathlib import Path
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

# Configuration depuis variables d'environnement
B2_KEY_ID = os.getenv('B2_KEY_ID')
B2_APPLICATION_KEY = os.getenv('B2_APPLICATION_KEY')
B2_BUCKET_NAME = os.getenv('B2_BUCKET_NAME')
B2_ENDPOINT_URL = os.getenv('B2_ENDPOINT_URL', 'https://s3.us-west-004.backblazeb2.com')
B2_REGION = os.getenv('B2_REGION', 'us-west-004')

SOURCE_DIR = 'vercel-blob-backup'

def check_credentials():
    """Vérifie que les credentials B2 sont configurés"""
    if not all([B2_KEY_ID, B2_APPLICATION_KEY, B2_BUCKET_NAME]):
        print("❌ Erreur: Credentials Backblaze B2 manquants")
        print("\n💡 Définissez les variables d'environnement:")
        print("   export B2_KEY_ID='your-key-id'")
        print("   export B2_APPLICATION_KEY='your-application-key'")
        print("   export B2_BUCKET_NAME='your-bucket-name'")
        return False
    return True

def upload_to_b2():
    """Upload tous les fichiers vers Backblaze B2"""
    print("🚀 Début de l'upload vers Backblaze B2...\n")
    
    # Connexion à B2
    try:
        s3 = boto3.client(
            's3',
            endpoint_url=B2_ENDPOINT_URL,
            aws_access_key_id=B2_KEY_ID,
            aws_secret_access_key=B2_APPLICATION_KEY,
            region_name=B2_REGION
        )
        
        # Vérifier que le bucket existe
        s3.head_bucket(Bucket=B2_BUCKET_NAME)
        print(f"✅ Connecté au bucket: {B2_BUCKET_NAME}\n")
        
    except NoCredentialsError:
        print("❌ Credentials invalides")
        return
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            print(f"❌ Bucket '{B2_BUCKET_NAME}' introuvable")
        else:
            print(f"❌ Erreur: {e}")
        return
    
    # Charger la liste des fichiers
    file_list_path = Path(SOURCE_DIR) / 'file-list.json'
    if not file_list_path.exists():
        print(f"❌ Fichier {file_list_path} introuvable")
        print("💡 Exécutez d'abord: node scripts/download-vercel-blob.js")
        return
    
    with open(file_list_path, 'r') as f:
        files = json.load(f)
    
    print(f"📦 {len(files)} fichiers à uploader\n")
    
    # Upload chaque fichier
    uploaded = 0
    skipped = 0
    errors = 0
    
    for file_info in files:
        filename = file_info['pathname']
        filepath = Path(SOURCE_DIR) / filename
        
        if not filepath.exists():
            print(f"⚠️  Fichier manquant: {filename}")
            skipped += 1
            continue
        
        try:
            # Déterminer le Content-Type
            content_type = 'application/octet-stream'
            if filename.endswith('.glb'):
                content_type = 'model/gltf-binary'
            elif filename.endswith('.gltf'):
                content_type = 'model/gltf+json'
            elif filename.endswith(('.jpg', '.jpeg')):
                content_type = 'image/jpeg'
            elif filename.endswith('.png'):
                content_type = 'image/png'
            
            # Upload
            print(f"⬆️  [{uploaded + 1}/{len(files)}] {filename}... ", end='')
            
            s3.upload_file(
                str(filepath),
                B2_BUCKET_NAME,
                filename,
                ExtraArgs={
                    'ContentType': content_type,
                    'ACL': 'public-read',
                    'CacheControl': 'max-age=86400'
                }
            )
            
            # URL publique
            public_url = f"{B2_ENDPOINT_URL}/{B2_BUCKET_NAME}/{filename}"
            print(f"✅ {public_url}")
            uploaded += 1
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
            errors += 1
    
    print(f"\n{'=' * 60}")
    print(f"✅ Upload terminé !")
    print(f"   - Uploadés: {uploaded}/{len(files)}")
    print(f"   - Ignorés: {skipped}")
    print(f"   - Erreurs: {errors}")
    print(f"{'=' * 60}\n")
    
    # Afficher URL de base
    print(f"🌐 URL de base des fichiers:")
    print(f"   {B2_ENDPOINT_URL}/{B2_BUCKET_NAME}/")

if __name__ == '__main__':
    if check_credentials():
        upload_to_b2()
