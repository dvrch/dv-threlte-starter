

# TYPE_CHOICES = ['box', 'torus', 'icosahedron', 'nissangame', 'bibigame', 'garden', 'bibi', 
#                 'vague', 'sphere', 'nissan', 'tissus', 'desk'] 
TYPE_CHOICES = [
    ('box', 'Box'),
    ('torus', 'Torus'),
    ('icosahedron', 'Icosahedron'),
    ('nissangame', 'Nissan Game'),
    ('bibigame', 'Bibi Game'),
    ('garden', 'Garden'),
    ('bibi', 'Bibi'),
    ('vague', 'Vague'),
    ('sphere', 'Sphere'),
    ('nissan', 'Nissan'),
    ('tissus', 'Tissus'),
    ('desk', 'Desk'),
]






"""
Il semble que vous rencontriez une erreur 404 lors de la tentative de chargement des types dans votre composant `AddGeometry.svelte`. Cela signifie que l'URL `http://localhost:8000/api/types/` ne renvoie pas de réponse valide. Voici quelques étapes pour résoudre ce problème :

1. **Vérifiez l'URL de l'API** : Assurez-vous que l'API est en cours d'exécution et que l'URL est correcte. Vous pouvez tester l'URL directement dans votre navigateur ou avec un outil comme Postman pour voir si elle renvoie des données.

2. **Vérifiez les routes de votre API** : Assurez-vous que la route `/api/types/` est bien définie dans votre application Django. Si cette route n'existe pas, vous devez l'ajouter.

3. **Ajoutez une vue pour les types** : Si vous n'avez pas encore de vue pour gérer les types, vous pouvez créer une nouvelle vue dans `views.py` pour renvoyer les types disponibles. Voici un exemple de code :

```python
# Base_threlte_dv/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .dv_config import TYPE_CHOICES

class TypeView(APIView):
    def get(self, request):
        types = [{'id': choice[0], 'name': choice[1]} for choice in TYPE_CHOICES]
        return Response(types)
```

4. **Ajoutez la route pour les types** : Ensuite, vous devez ajouter cette vue à vos URLs dans `urls.py` :

```python
# Base_threlte_dv/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GeometryViewSet, TypeView

router = DefaultRouter()
router.register('geometries', GeometryViewSet, basename='geometries')

urlpatterns = [
    path('types/', TypeView.as_view(), name='types'),  # Ajoutez cette ligne
    path('', include(router.urls)),
]
```

5. **Mettez à jour votre composant Svelte** : Assurez-vous que votre composant `AddGeometry.svelte` utilise la bonne URL pour charger les types.

Voici les modifications nécessaires dans votre fichier `AddGeometry.svelte` :

```svelte
// ... code existant ...
const loadTypes = async () => {
    const response = await fetch('http://localhost:8000/types/'); // Mettez à jour l'URL ici
    if (!response.ok) {
        throw new Error('Failed to fetch types');
    }
    
    types = await response.json();
};
// ... code existant ...
```

### Résumé des modifications
- Ajout d'une vue `TypeView` pour gérer les types.
- Mise à jour des URLs dans `urls.py` pour inclure la nouvelle route.
- Modification de l'URL dans `AddGeometry.svelte` pour correspondre à la nouvelle route.

Ces changements devraient résoudre l'erreur 404 que vous rencontrez. Si vous avez d'autres questions ou si vous avez besoin d'aide supplémentaire, n'hésitez pas à demander !

"""