# Documentation de la Route `/bibi`

Ce document a pour but de clarifier la structure et le contenu du dossier `/src/routes/bibi/`, qui semble servir de hub pour diverses expériences avec Three.js et Threlte.

---

## État Actuel et Analyse des Erreurs

Actuellement, la page `/bibi` est **cassée**. 

L'analyse des erreurs de la console montre que le fichier principal `+page.svelte` essaie de charger le composant `demo_01.svelte`. Cependant, `demo_01.svelte` n'est pas un composant Svelte valide mais une page HTML complète qui, de plus, tente de charger un script (`demo_01.js`) depuis un chemin inaccessible (`/src/...`).

**Ceci est la source principale des erreurs `404 Not Found` et des avertissements de `props` inconnues.**

---

## Arborescence et Description des Fichiers

Voici une description du rôle probable de chaque fichier dans ce répertoire.

```
/src/routes/bibi/
|-- +page.svelte        # Point d'entrée principal de la route /bibi.
|-- +page.ts            # Fichier de configuration de la page (active le prerendering).
|
|-- demo_01.svelte      # (Actuellement utilisé et cassé) Fichier HTML erroné.
|
|-- bibanime.svelte     # Composants Svelte/Threlte plus complexes, 
|-- bibi.svelte         # probablement des expériences alternatives ou des
|-- tissus-simulat.svelte # versions de travail.
|-- demo_09.svelte      #
|-- demoxx.svelte       #
|-- ge.svelte           #
|-- page2.svelte        #
|
|-- demo_01.js          # Fichier JS vide ou non pertinent.
|-- demo_01.ts          # Logique Three.js pure (non intégrée à Svelte).
|-- demo_02.ts          # ...
|-- demo_03.ts          # ...
|-- demo_04.ts          # Suite de scripts contenant diverses scènes
|-- demo_05.ts          # et logiques Three.js. Semblent être des
|-- demo_06.ts          # tests unitaires ou des exemples.
|-- demo_07.ts          # ...
|-- demo_08.ts          # ...
|-- demo_09.ts          # ...
|-- demo_10.ts          # ...
|-- demo_11.ts          # ...
|-- demo_12.ts          #
|
|-- ___page.svelte      # Ancienne version de la page, renommée pour être inactive.
```

### Catégories de Fichiers

- **Fichiers Actifs :** `+page.svelte`, `+page.ts`.
- **Cause de l'Erreur :** `demo_01.svelte` (utilisé par `+page.svelte`).
- **Expériences Alternatives (Composants Svelte) :** `bibanime.svelte`, `tissus-simulat.svelte`, etc. Ce sont des composants plus complets qui pourraient fonctionner s'ils étaient correctement intégrés.
- **Expériences Alternatives (Scripts Purs) :** La série `demo_XX.ts` contient de la logique Three.js qui n'est pas directement utilisable en tant que composant Svelte.

---

## Plan de Correction Suggéré

Pour rendre la page `/bibi` de nouveau fonctionnelle, voici les étapes proposées :

1.  **Réécrire `demo_01.svelte`** : Transformer ce fichier en un composant Svelte/Threlte valide qui affiche une scène de base (par exemple, un simple cube), et qui accepte les `props` (`position`, `rotation`) qui lui sont passées.
2.  **Nettoyer les Avertissements** : Ajouter `export let data;` à `+page.svelte` pour résoudre les avertissements restants.

Cela fournira une base stable et fonctionnelle. Ensuite, si vous le souhaitez, nous pourrons remplacer le contenu de `demo_01.svelte` par une des autres expériences plus complexes comme `bibanime.svelte`.
