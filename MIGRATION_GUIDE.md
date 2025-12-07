# 🚀 Guide de Migration - Architecture Hybride avec Cloudinary

## 📋 Vue d'ensemble

Migration vers **Cloudinary** (100% gratuit, **SANS carte bancaire**) + **Railway** (Django) + **Vercel** (Frontend).

---

## ✅ Phase 1 : Configuration (COMPLÉTÉE)

### Fichiers créés/modifiés
- ✅ [`scripts/upload-to-cloudinary.py`](file:///home/kd/Bureau/dv-threlte-starter/scripts/upload-to-cloudinary.py) - Upload vers Cloudinary
- ✅ [`requirements.txt`](file:///home/kd/Bureau/dv-threlte-starter/requirements.txt) - Dépendances Cloudinary
- ✅ [`backend/settings.py`](file:///home/kd/Bureau/dv-threlte-starter/backend/settings.py) - Config Django Cloudinary
- ✅ [`.env.production`](file:///home/kd/Bureau/dv-threlte-starter/.env.production) - Variables Cloudinary
- ✅ [`railway.toml`](file:///home/kd/Bureau/dv-threlte-starter/railway.toml) - Déploiement Railway

---

## 🎨 Phase 2 : Créer Compte Cloudinary (GRATUIT)

### Étape 1 : Inscription (sans CB)

1. **Aller sur** : [cloudinary.com/users/register_free](https://cloudinary.com/users/register_free)
2. **S'inscrire avec** : Email ou GitHub
3. **Plan** : Free (automatique) - **Aucune CB demandée** ✅

### Étape 2 : Récupérer Credentials

1. Aller dans **Dashboard** (après connexion)
2. Cliquer sur **Settings** (⚙️ en haut à droite)
3. Aller dans **Access Keys**
4. Noter :
   - **Cloud Name** : `dxxxxx` (ou nom personnalisé)
   - **API Key** : `123456789012345`
   - **API Secret** : `AbCdEfGhIjKlMnOpQrStUvWxYz` (cliquer sur 👁️ pour voir)

### Étape 3 : Configurer Variables Locales

```bash
# Dans .env local (pour tester upload)
echo 'CLOUDINARY_CLOUD_NAME=ton-cloud-name' >> .env
echo 'CLOUDINARY_API_KEY=ton-api-key' >> .env
echo 'CLOUDINARY_API_SECRET=ton-api-secret' >> .env
```

---

## 📤 Phase 3 : Upload Fichiers vers Cloudinary

### Option A : Upload Automatique (Recommandé)

```bash
# 1. Installer dépendances
pip install cloudinary

# 2. Configurer credentials (ou utiliser .env)
export CLOUDINARY_CLOUD_NAME=ton-cloud-name
export CLOUDINARY_API_KEY=ton-api-key
export CLOUDINARY_API_SECRET=ton-api-secret

# 3. Upload tous les fichiers depuis static/
python scripts/upload-to-cloudinary.py
```

Le script uploade automatiquement :
- `static/models/*.glb` → Fichiers 3D
- `static/assets/*` → Images
- `static/public/*` → Autres assets

### Option B : Upload Manuel (Interface Web)

1. Aller sur [cloudinary.com/console/media_library](https://cloudinary.com/console/media_library)
2. Cliquer **Upload**
3. Glisser-déposer fichiers
4. Créer un dossier `dv-threlte` pour organiser

---

## 🚂 Phase 4 : Déploiement Backend sur Railway

### Étape 1 : Créer projet Railway

1. [railway.app](https://railway.app/) → **Sign up with GitHub**
2. **New Project** → **Deploy from GitHub repo**
3. Sélectionner `dvrch/dv-threlte-starter`

### Étape 2 : Ajouter PostgreSQL

1. **New** → **Database** → **PostgreSQL**
2. Railway génère `DATABASE_URL` automatiquement

### Étape 3 : Variables d'Environnement

Dans **Railway Dashboard > Variables**, ajouter :

```bash
# Django
SECRET_KEY=changez-moi-avec-cle-longue-aleatoire
DEBUG=False
ALLOWED_HOSTS=.railway.app,.vercel.app

# Cloudinary
USE_CLOUDINARY=True
CLOUDINARY_CLOUD_NAME=ton-cloud-name
CLOUDINARY_API_KEY=ton-api-key
CLOUDINARY_API_SECRET=ton-api-secret

# CORS
CORS_ALLOWED_ORIGINS=https://dv-threlte-starter.vercel.app,http://localhost:5173
```

### Étape 4 : Déployer

Railway détecte `railway.toml` et déploie automatiquement.

**Tester** :
```bash
curl https://[ton-app].up.railway.app/api/health
# Expected: {"status": "ok"}
```

---

## 🌐 Phase 5 : Mise à jour Frontend Vercel

### Dans Vercel Dashboard

1. **Settings** → **Environment Variables**
2. Modifier `VITE_API_URL` :
   ```
   VITE_API_URL=https://[ton-app].up.railway.app
   ```
3. **Redéployer** : Deployments → ... → Redeploy

---

## 🧪 Test Complet

### 1. Backend Django
```bash
curl https://[ton-app].up.railway.app/api/health
```

### 2. Upload Fichier 3D
```bash
curl -X POST https://[ton-app].up.railway.app/api/upload \
  -F "file=@test.glb"
# {"url": "https://res.cloudinary.com/.../test.glb", "status": "success"}
```

### 3. Frontend
1. Ouvrir `https://dv-threlte-starter.vercel.app`
2. Tester formulaire upload
3. Vérifier chargement modèles 3D

---

## 💰 Coûts

| Service | Plan | Coût/mois |
|---------|------|-----------|
| **Cloudinary** | Free | **$0** (25GB, sans CB) |
| **Railway** | Crédits | **$0** puis ~$5-10 |
| **Vercel** | Hobby | **$0** |
| **Neon PostgreSQL** | Free | **$0** |

**Total** : $0 initialement, ~$5-10/mois après crédits Railway

---

## 🆘 Dépannage

### ❌ "Invalid Cloudinary credentials"
- Vérifier `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`
- Vérifier qu'il n'y a pas d'espaces dans les valeurs

### ❌ Upload échoue
- Vérifier que `USE_CLOUDINARY=True` sur Railway
- Vérifier quota Cloudinary (Dashboard → Usage)

### ❌ CORS Error
- Vérifier `CORS_ALLOWED_ORIGINS` inclut URL Vercel
- Vérifier `ALLOWED_HOSTS` inclut `.railway.app`

---

## 🎁 Avantages Cloudinary

- ✅ **Gratuit sans CB** (25 GB)
- ✅ **CDN mondial** automatique
- ✅ **Optimisation images** gratuite
- ✅ **Pas de limite bande passante** (plan Free)
- ✅ **Interface drag & drop**
- ✅ **Support fichiers 3D** (.glb, .gltf)

---

## 📚 Ressources

- [Cloudinary Docs](https://cloudinary.com/documentation)
- [Railway Docs](https://docs.railway.app/)
- [django-cloudinary-storage](https://django-cloudinary-storage.readthedocs.io/)
