refactor(models): Simplification de la logique du modèle Geometry

Ce commit refactorise le modèle `Geometry` pour supprimer une logique complexe et non standard de génération de type par défaut, et nettoie les migrations associées.

Modifications principales :
- Suppression de la fonction `write_type_py` et de sa logique de génération de fichier dynamique.
- Le champ `type` du modèle utilise maintenant une valeur par défaut statique ('box') au lieu d'une valeur dynamique.
- Le champ `name` n'est plus unique et n'a plus de valeur par défaut liée à l'ancienne logique.
- Nettoyage des imports (`os`, `ctypes`, `type_py`) devenus inutiles dans `models.py`.
- Suppression d'un ancien fichier de migration qui était lié à la logique retirée.
