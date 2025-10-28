# Guide de Déploiement sur Vercel

Ce guide explique comment déployer l'application (frontend SvelteKit + backend Django) sur Vercel.

## Résumé des Préparations

Le projet a été configuré pour le déploiement :
- **Monorepo**: Frontend et backend dans le même dépôt.
- **Configuration Vercel**: Un fichier `vercel.json` a été ajouté pour gérer les builds et le routage.
- **Dépendances Python**: Le fichier `requirements.txt` a été unifié.
- **Paramètres Django**: Le fichier `settings.py` est prêt pour la production (base de données, secret key, etc.).
- **Frontend SvelteKit**: Les appels API utilisent des URLs relatives (`/api/...`).

---

## ✅ Votre Guide de Déploiement Final

Suivez ces étapes pour mettre votre site en ligne.

### 1. Créer votre base de données de production

1.  Allez sur votre tableau de bord [Vercel](https://vercel.com/dashboard).
2.  Allez dans l'onglet **Storage** et créez une nouvelle base de données **Postgres**.
3.  Donnez-lui un nom et choisissez une région.
4.  Une fois créée, Vercel vous montrera les détails de connexion. Copiez l'URL qui ressemble à `postgres://...`. Ce sera votre `DATABASE_URL`.

### 2. Pousser votre code sur GitHub

Assurez-vous que toutes les modifications sont bien envoyées sur votre dépôt GitHub.

```bash
git add .
git commit -m "feat: Configure project for Vercel deployment"
git push
```

### 3. Déployer sur Vercel

1.  Dans votre tableau de bord Vercel, cliquez sur **Add New...** -> **Project**.
2.  Importez votre dépôt GitHub.
3.  Vercel devrait automatiquement détecter **SvelteKit** comme framework. C'est correct.
4.  Dépliez la section **Environment Variables**. C'est ici que vous devez ajouter vos secrets :
    *   **Clé 1 :**
        *   Nom : `DATABASE_URL`
        *   Valeur : *Collez l'URL de votre base de données Vercel Postgres que vous avez copiée.*
    *   **Clé 2 :**
        *   Nom : `SECRET_KEY`
        *   Valeur : *Générez une nouvelle clé secrète Django (par exemple, via [ce site](https://djecrety.ir/)) et collez-la ici.*
5.  Cliquez sur **Deploy**. Vercel va maintenant construire et déployer votre site.

### 4. Finaliser la base de données (Migrations et Super-utilisateur)

Une fois le déploiement terminé, votre site est en ligne, mais la base de données est vide.

La méthode la plus simple est de le faire depuis votre machine locale :

1.  **Sur votre machine locale**, ouvrez le fichier `backend/films_backend/films_backend/settings.py`.
2.  **Temporairement**, commentez la configuration `DATABASES` existante et remplacez-la par celle-ci, en utilisant votre URL de production :

    ```python
    # DATABASES = { ... } # Commentez l'ancienne configuration
    DATABASES = {
        'default': dj_database_url.parse('VOTRE_DATABASE_URL_DE_VERCEL')
    }
    ```

3.  Ouvrez un terminal **dans votre environnement virtuel Python local** (`source backend/venv-backend/bin/activate`).
4.  Naviguez dans le dossier du backend : `cd backend/films_backend`
5.  Exécutez les migrations sur la base de données de production :

    ```bash
    python manage.py migrate
    ```

6.  Créez votre compte administrateur :

    ```bash
    python manage.py createsuperuser
    ```
    Suivez les instructions pour créer votre utilisateur.

7.  **TRÈS IMPORTANT :** Une fois terminé, **annulez les modifications** dans votre fichier `settings.py` pour remettre la configuration d'origine.

Votre application est maintenant entièrement fonctionnelle en ligne ! Vous pouvez accéder à l'interface d'administration via `https://<votre-url-vercel>/admin`.
