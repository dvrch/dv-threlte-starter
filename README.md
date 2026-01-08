# 💎 DV-Threlte-Starter 🚀

Bienvenue dans le futur de la **3D sur le Web** ! 🌐✨ 

Ce projet est un environnement de création et de visualisation 3D ultra-fluide qui transforme ton navigateur en un véritable **studio d'édition temps réel** 🎮.

---

## 🌟 Points Forts
- **Rendu Cinématique** : Effets **Premium** (Bloom, Réflexions HDR, Iridescence) pour un look "AAA" 💎.
- **Portabilité Totale** : Ton travail te suit partout ! Exporte et importe ton monde en un clic 💾.
- **Import Haute-Vitesse** : Glisse un fichier **.GLB** et regarde-le prendre vie instantanément 🏗️.
- **Contrôles Professionnels** : Gizmos de transformation (P, R, S) pour un placement au pixel près 🛠️.

---

## 📂 Portabilité & "Database Client"
C'est la fonctionnalité magique ! 🪄
- **Exportation** : Une fois ton monde construit (positions, rotations, échelles), clique sur `Exporter (JSON)`. Tu obtiens un fichier qui contient toute la "mémoire" de ta scène.
- **Importation** : De retour plus tard ? Clique sur `Importer (JSON)`, choisis ton fichier, et ton monde se reconstruit exactement comme tu l'as laissé ! 🔄✨

---

## 🛠️ Guide du Développeur

### 📥 Installation
1. Clone le projet : `git clone ...`
2. Installe **pnpm** (recommandé) : `npm install -g pnpm`
3. Installe les dépendances : `pnpm install`
4. Lance le mode dev : `pnpm dev`

### 🏗️ Développer et Personnaliser : "Database-First" 🗄️
Vous pouvez maintenant utiliser un gestionnaire de base de données externe (ex: **DB Browser for SQLite**) pour modifier vos objets.

1.  Ouvrez `static/data/inventory.sqlite` dans votre logiciel favori.
2.  Modifiez vos types, positions, couleurs ou chemins (`model_url`).
3.  Lancez la commande magique pour appliquer vos changements à l'app :
    ```bash
    pnpm db:push
    ```
4.  Votre application est à jour ! 🚀

| Commande | Action |
| :--- | :--- |
| `pnpm dev` | Lancer le serveur de développement 🚀 |
| `pnpm db:pull` | Synchroniser (écraser) depuis l'API distante 📡 |
| `pnpm db:push` | Appliquer vos modifs SQLite locales à l'App 🏗️ |
| `pnpm build` | Compiler pour la production 🏗️ |

---

## 🤝 Contribution & Participation
Tu veux améliorer le moteur ? C'est avec plaisir ! 🕺💨
- **Issues** : Un bug ? Une idée folle ? [Ouvre une Issue](https://github.com/dvrch/dv-threlte-starter/issues) !
- **Pull Requests** : Les contributeurs sont cités avec fierté dans le code. N'hésite pas à proposer tes améliorations de shaders ou de composants.
- **Crédits** : Ce projet utilise Threlte (Three.js pour Svelte). Merci à la communauté open-source !

---

## 📜 Licence & Protection
Ce projet est sous licence **MIT**. 
> C'est la licence la plus cool : tu peux l'utiliser, le modifier et le partager librement, tant que tu cites l'auteur original. C'est parfait pour valoriser ton profil de dev tout en protégeant l'intégrité de ton travail ! 🛡️✅

---

## 📊 Tableau de Bord Statique
Accède aux snapshots de ton monde générés lors du dernier déploiement :
- [📋 Inventaire Visuel](https://dvrch.github.io/dv-threlte-starter/data/inventory.html)
- [💾 Télécharger la Base (.sqlite)](https://dvrch.github.io/dv-threlte-starter/data/inventory.sqlite)

---

Prêt à construire ton propre univers ? **Fonce !** 🕺💨
