import requests
import os
from dotenv import load_dotenv
from pathlib import Path

# Charger les variables d'environnement depuis le fichier .env parent
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(env_path)

def test_model_upload():
    # Vérifier que le token est disponible
    token = os.getenv('BLOB_READ_WRITE_TOKEN')
    if not token:
        print("ERREUR: BLOB_READ_WRITE_TOKEN non trouvé dans .env")
        print("Chemin du .env cherché:", env_path)
        return
    print("Token Vercel Blob trouvé :", token[:10] + "...")
    # 1. Obtenir l'URL présignée pour l'upload
    upload_response = requests.post(
        'http://localhost:8000/api/upload/',
        json={
            'filename': 'test-model.glb',
            'type': 'glb'
        }
    )
    
    if upload_response.status_code != 200:
        print("Erreur lors de l'obtention de l'URL présignée:", upload_response.text)
        return
    
    upload_data = upload_response.json()
    print("URL présignée obtenue:", upload_data)
    
    # 2. Simuler l'upload d'un modèle (ici nous créons un petit fichier test)
    test_content = b'Test GLB content'  # Dans un cas réel, ce serait le contenu du fichier GLB
    
    put_response = requests.put(
        upload_data['url'],
        data=test_content,
        headers={'Content-Type': 'application/octet-stream'}
    )
    
    if put_response.status_code != 200:
        print("Erreur lors de l'upload du fichier:", put_response.text)
        return
    
    print("Fichier uploadé avec succès!")
    
    # 3. Créer une nouvelle géométrie avec l'URL du modèle
    geometry_response = requests.post(
        'http://localhost:8000/api/geometries/',
        json={
            'name': 'Test 3D Model',
            'model_url': upload_data['url'],
            'model_type': 'glb',
            'position': {'x': 0, 'y': 0, 'z': 0},
            'rotation': {'x': 0, 'y': 0, 'z': 0},
            'type': 'cube'  # ou un autre type de votre TYPE_CHOICES
        }
    )
    
    if geometry_response.status_code != 201:
        print("Erreur lors de la création de la géométrie:", geometry_response.text)
        return
    
    print("Géométrie créée avec succès:", geometry_response.json())

if __name__ == '__main__':
    test_model_upload()
