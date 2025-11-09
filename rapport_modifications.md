feat(assets): Ajout de ressources statiques et affinements du rendu 3D

Ce commit intègre de nombreuses nouvelles ressources statiques et poursuit l'optimisation de l'architecture de rendu 3D, améliorant la gestion des assets et des interactions utilisateur.

Modifications principales :
- **Ajout de ressources statiques :**
  - Intégration d'une collection d'images (JPG, PNG, WEBP), d'un fichier de police (`font.json`), d'un fichier de licence (`license_bibi.txt`) et du fichier `robots.txt` dans `static/public/`.

- **Affinements de l'architecture de rendu 3D :**
  - Poursuite des ajustements dans `Dynamic3DModel.svelte` et les layouts (`src/routes/app/+layout.svelte`, `src/routes/app/+page.svelte`) pour une gestion plus flexible du `<Canvas>` et des modèles 3D.
  - Corrections de chemins d'accès aux assets audio dans `src/routes/about/block.js`.
  - Ajustements dans des composants spécifiques comme `tissus-simulat.svelte`, `desksc/+page.svelte`, `sphere/+page.svelte` pour s'aligner avec la nouvelle architecture de rendu.

- **Configuration du projet :**
  - Mise à jour du `.gitignore` pour inclure `rapport_modifications.md` et `.___.md`.
