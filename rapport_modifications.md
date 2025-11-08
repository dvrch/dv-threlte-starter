refactor(3d-rendering): Affinements de l'architecture 3D et gestion des assets

Ce commit poursuit l'optimisation de l'architecture de rendu 3D et améliore la gestion des assets et des interactions utilisateur.

Modifications détaillées :
- **Gestion du Canvas et des interactions :**
  - Le composant `<Canvas>` dans `src/routes/app/+layout.svelte` est désormais encapsulé dans un `div` pour une gestion plus fine des `pointer-events`, séparant les interactions 3D de l'interface utilisateur.
  - Les composants `desksc/+page.svelte` et `sphere/+page.svelte` ont été adaptés pour s'intégrer dans un `<Canvas>` parent, supprimant leur propre wrapper `<Canvas>`.

- **Refactorisation des modèles dynamiques :**
  - Dans `src/lib/components/Dynamic3DModel.svelte`, les composants Threlte sont maintenant référencés avec le préfixe `ThrelteT` (ex: `<ThrelteT.Mesh>`), et la logique de chargement dynamique a été ajustée.
  - Le chargement de texture dynamique dans `src/routes/bibi/tissus-simulat.svelte` a été temporairement désactivé (mis en commentaire).

- **Gestion des assets et chemins :**
  - Les chemins des fichiers audio dans `src/routes/about/block.js` ont été corrigés pour utiliser des chemins absolus (`/sound/`).
  - Ajout de `rapport_modifications.md` et `.___.md` au `.gitignore` pour exclure les fichiers de rapport et temporaires.

- **Passage de données :**
  - Ajout des exports `params`, `position`, `rotation`, `scale` dans `src/routes/app/+page.svelte` pour une flexibilité accrue dans le passage de données.