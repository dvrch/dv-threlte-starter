import os
import requests
from dotenv import load_dotenv

load_dotenv()

def upload_ghost_model():
    # URL de l'API
    url = 'http://localhost:8000/api/upload-blob/'
    
    # Chemin vers le fichier ghost.glb
    file_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'models', 'ghost.glb')
    
    print(f"Checking file path: {file_path}")
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return
    
    print("File found, preparing upload...")
    
    try:
        # Ouvrir et envoyer le fichier
        with open(file_path, 'rb') as file:
            files = {'file': ('ghost.glb', file, 'model/gltf-binary')}
            
            print("Sending request to server...")
            response = requests.post(url, files=files)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {response.headers}")
            
            try:
                print(f"Response Content: {response.text}")
                if response.headers.get('content-type') == 'application/json':
                    print(f"JSON Response: {response.json()}")
            except Exception as e:
                print(f"Error parsing response: {str(e)}")
                
    except Exception as e:
        print(f"Error during upload: {str(e)}")

if __name__ == "__main__":
    upload_ghost_model()
