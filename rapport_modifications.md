refactor(3d-rendering): Unification de la gestion des modèles 3D et optimisation du Canvas

Ce commit apporte une refonte majeure de l'architecture de rendu 3D, centralisant la gestion des modèles et optimisant l'utilisation du composant `<Canvas>`. L'objectif est d'améliorer la flexibilité, la performance et la maintenabilité du système de rendu.

Modifications détaillées :
- **Architecture de rendu 3D unifiée :**
  - Le composant `Dynamic3DModel.svelte` a été étendu pour gérer dynamiquement le rendu de divers types de modèles (GLTF, primitives, composants Svelte spécifiques) via une `componentMap`.
  - De nombreux composants de scène (`bibigame.svelte`, `nissangame.svelte`, `scene.svelte`, `vague/+page.svelte`, `desksc/+page.svelte`) ont été modifiés pour ne plus inclure leur propre `<Canvas>`, s'intégrant désormais dans un `<Canvas>` parent unique.

- **Gestion du Canvas et UI :**
  - Le `<Canvas>` principal dans `src/routes/app/+layout.svelte` a été configuré avec `pointer-events: none;` et l'overlay UI avec `pointer-events: auto;` pour une meilleure interaction utilisateur.
  - Le composant `bloom.svelte` expose désormais des props (`height`, `width`, `mipmapBlur`) pour une configuration externe de l'effet Bloom.

- **Améliorations des composants spécifiques :**
  - `spaceship.svelte` : Ajout de vérifications de nullité pour `gltf.nodes.Cube.material` et ajustement du chemin de texture.
  - `about/+page.svelte` : Initialisation de Rapier et définition explicite de la gravité pour le monde physique.
  - `sphere/+page.svelte` : Intégration de la caméra et des contrôles Orbit directement dans le `<Canvas>`.
  - `bibi/+page.svelte`, `desksc/+page.svelte`, `vague/+page.svelte` : Ajout des exports `data` et `params` pour la compatibilité avec les layouts SvelteKit.

- **Documentation :**
  - Mise à jour d'un chemin d'image dans `src/routes/mdwd/Montage de projet Djontso victorien 15_08_2O24.md`.
