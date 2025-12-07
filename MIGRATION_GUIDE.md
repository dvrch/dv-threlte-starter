# 🚀 Guide de Migration - Architecture Hybride

## 📋 Vue d'ensemble

Ce guide vous accompagne pour migrer de Vercel Blob vers une architecture hybride avec **Railway (Django)** + **Backblaze B2 (Stockage)** + **Vercel (Frontend)**.

---

## ✅ Phase 1 : Configuration (COMPLÉTÉE)

Les fichiers suivants ont été créés/modifiés :

### Fichiers créés
- ✅ [`scripts/download-vercel-blob.js`](file:///home/kd/Bureau/dv-threlte-starter/scripts/download-vercel-blob.js) - Téléchargement Vercel Blob
- ✅ [`scripts/upload-to-b2.py`](file:///home/kd/Bureau/dv-threlte-starter/scripts/upload-to-b2.py) - Upload vers Backblaze B2
- ✅ [`railway.toml`](file:///home/kd/Bureau/dv-threlte-starter/railway.toml) - Config déploiement Railway
- ✅ [`.env.production`](file:///home/kd/Bureau/dv-threlte-starter/.env.production) - Variables production

### Fichiers modifiés
- ✅ [`requirements.txt`](file:///home/kd/Bureau/dv-threlte-starter/requirements.txt) - Ajout `django-storages[s3]`, `boto3`
- ✅ [`backend/settings.py`](file:///home/kd/Bureau/dv-threlte-starter/backend/settings.py) - Config Backblaze B2
- ✅ [`.gitignore`](file:///home/kd/Bureau/dv-threlte-starter/.gitignore) - Ignore fichiers lourds

---

## 🔄 Phase 2 : Migration des Fichiers

### Étape 1 : Télécharger depuis Vercel Blob

```bash
# 1. Installer dépendances
npm install @vercel/blob

# 2. Récupérer le token dans Vercel Dashboard
# Vercel > Storage > Blob > Settings > Read/Write Token

# 3. Télécharger tous les fichiers
BLOB_READ_WRITE_TOKEN=vercel_blob_rw_xxx node scripts/download-vercel-blob.js
```

**Résultat** : Dossier `vercel-blob-backup/` avec tous vos fichiers + `file-list.json`

### Étape 2 : Créer compte Backblaze B2

1. **Inscription** : [backblaze.com/b2/sign-up.html](https://www.backblaze.com/b2/sign-up.html)
2. **Créer un Bucket** :
   - Nom : `dv-threlte-assets` (ou autre)
   - Région : `us-west-004` (recommandé)
   - Visibilité : **Public**
3. **Générer Application Key** :
   - Menu : Account > Application Keys
   - Créer nouvelle clé avec accès Read/Write
   - **Noter** : `keyID` et `applicationKey` (ne seront plus affichés)

### Étape 3 : Upload vers Backblaze B2

```bash
# 1. Configurer credentials
export B2_KEY_ID=your-key-id-here
export B2_APPLICATION_KEY=your-application-key-here
export B2_BUCKET_NAME=dv-threlte-assets

# 2. Uploader tous les fichiers
python scripts/upload-to-b2.py
```

**Résultat** : Tous vos fichiers sont maintenant sur B2 avec URLs publiques

---

## 🚂 Phase 3 : Déploiement Backend sur Railway

### Étape 1 : Créer projet Railway

1. Aller sur [railway.app](https://railway.app/)
2. **Sign up with GitHub**
3. **New Project** > **Deploy from GitHub repo**
4. Sélectionner `dvrch/dv-threlte-starter`

### Étape 2 : Ajouter PostgreSQL

1. Dans votre projet Railway : **New** > **Database** > **PostgreSQL**
2. Railway génère automatiquement `DATABASE_URL`

### Étape 3 : Configurer Variables d'Environnement

Dans Railway Dashboard > **Variables**, ajouter :

```bash
# Django Core
SECRET_KEY=changez-moi-avec-une-cle-secrete-longue
DEBUG=False
DJANGO_SETTINGS_MODULE=backend.settings
ALLOWED_HOSTS=.railway.app,.vercel.app

# Backblaze B2
USE_B2_STORAGE=True
B2_KEY_ID=votre-key-id-b2
B2_APPLICATION_KEY=votre-application-key-b2
B2_BUCKET_NAME=dv-threlte-assets
B2_ENDPOINT_URL=https://s3.us-west-004.backblazeb2.com
B2_REGION=us-west-004

# CORS
CORS_ALLOWED_ORIGINS=https://dv-threlte-starter.vercel.app,http://localhost:5173
```

### Étape 4 : Déployer

Railway détecte automatiquement `railway.toml` et déploie Django.

**Vérifier** : Copier l'URL publique (ex: `https://dv-threlte-starter-backend.up.railway.app`)

```bash
curl https://dv-threlte-starter-backend.up.railway.app/api/health
# Expected: {"status": "ok"}
```

---

## 🌐 Phase 4 : Mise à jour Frontend

### Dans Vercel Dashboard

1. **Settings** > **Environment Variables**
2. Modifier `VITE_API_URL` :
   ```
   VITE_API_URL=https://dv-threlte-starter-backend.up.railway.app
   ```
3. **Redéployer** : Deployments > ... > Redeploy

### Test Frontend → Backend

Ouvrir l'app Vercel et vérifier dans DevTools (Network) que les appels API pointent vers Railway.

---

## 🧹 Phase 5 : Nettoyage Git (Optionnel)

> [!CAUTION]
> Cette étape est **irréversible** et réécrit l'historique Git

```bash
# 1. Sauvegarder d'abord
git clone https://github.com/dvrch/dv-threlte-starter backup-repo

# 2. Installer git-filter-repo
pip install git-filter-repo

# 3. Nettoyer fichiers lourds de l'historique
git filter-repo --path-glob '*.glb' --invert-paths --force
git filter-repo --path-glob '*.blend' --invert-paths --force
git filter-repo --path-glob '*.bin' --invert-paths --force

# 4. Force push (⚠️ ATTENTION)
git remote add origin https://github.com/dvrch/dv-threlte-starter
git push origin --force --all

# 5. Nettoyer cache local
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

---

## ✅ Vérification Finale

### Backend Django
```bash
curl https://[votre-app].up.railway.app/api/health
# {"status": "ok"}
```

### Upload Fichier 3D
```bash
curl -X POST https://[votre-app].up.railway.app/api/upload \
  -F "file=@test.glb" \
  -H "Content-Type: multipart/form-data"
# {"url": "https://s3...backblazeb2.com/.../test.glb", "status": "success"}
```

### Frontend Vercel
1. Ouvrir app : `https://dv-threlte-starter.vercel.app`
2. Tester formulaire upload
3. Vérifier chargement modèles 3D

---

## 📊 Coûts Estimés

| Service | Plan | Coût/mois |
|---------|------|-----------|
| **Vercel** (Frontend) | Hobby | **$0** |
| **Railway** (Backend) | Crédits gratuits | **$0** puis ~$5-10 |
| **Backblaze B2** | 10GB gratuit | **$0** puis ~$0.50 |
| **Neon PostgreSQL** | Gratuit | **$0** |

**Total** : ~$5-10/mois après crédits gratuits

---

## 🆘 Dépannage

### ❌ Erreur "Invalid Credentials" (Railway)
- Vérifier que `SECRET_KEY` est défini
- Vérifier `DJANGO_SETTINGS_MODULE=backend.settings`

### ❌ CORS Error (Frontend → Backend)
- Vérifier `CORS_ALLOWED_ORIGINS` inclut URL Vercel
- Vérifier `ALLOWED_HOSTS` inclut `.railway.app`

### ❌ Upload fichier échoue
- Vérifier `USE_B2_STORAGE=True`
- Vérifier credentials B2 valides
- Vérifier bucket existe et est public

---

## 📚 Ressources

- [Railway Docs](https://docs.railway.app/)
- [Backblaze B2 Docs](https://www.backblaze.com/b2/docs/)
- [django-storages](https://django-storages.readthedocs.io/)
