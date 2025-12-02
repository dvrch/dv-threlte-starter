# 🚀 Guide Complet de Déploiement - Frontend + Backend sur Vercel

## 📊 Architecture Finale

```
┌─────────────────────────────────────────────────────┐
│                    Navigateur                        │
│              (votre-app.vercel.app)                 │
└────────────────────┬────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
   ┌─────────┐             ┌──────────────┐
   │ SvelteKit│             │  Django API  │
   │Frontend  │─────────────│   Backend    │
   │ Vercel   │   fetch()   │   Vercel     │
   │          │             │  /api/*      │
   └─────────┘             └──────┬───────┘
                                   │
                                   ▼
                          ┌─────────────────┐
                          │   Neon DB       │
                          │   PostgreSQL    │
                          └─────────────────┘
```

---

## 🎯 Étape 1: Configuration en Développement Local

### Option A: Lancement manuel (2 terminaux)

**Terminal 1 - Django Backend:**
```bash
cd backend
python manage.py runserver 0.0.0.0:8000
```

**Terminal 2 - SvelteKit Frontend:**
```bash
npm run dev
# Accessible sur http://localhost:5173
```

### Option B: Utiliser le script automatisé

```bash
chmod +x dev.sh
./dev.sh
```

**Le fichier `.env.local` a été créé automatiquement avec:**
```
PUBLIC_API_URL="http://localhost:8000"
PUBLIC_STATIC_URL="https://w0cb58ft2bj7sg0v.public.blob.vercel-storage.com"
```

---

## 🌐 Étape 2: Variables d'Environnement

### Pour le Frontend SvelteKit (Vercel Dashboard)

**Settings > Environment Variables:**

```
PUBLIC_API_URL = https://votre-api-django.vercel.app
PUBLIC_STATIC_URL = https://w0cb58ft2bj7sg0v.public.blob.vercel-storage.com
```

### Pour le Backend Django (Vercel Dashboard)

**Settings > Environment Variables:**

```
DEBUG = False
SECRET_KEY = votre-cle-secrete-django
DATABASE_URL = postgresql://... (déjà configuré avec Neon)
BLOB_READ_WRITE_TOKEN = votre-token-vercel
STORE_ID = store_W0CB58Ft2bj7Sg0v
VERCEL_URL = votre-api-django.vercel.app
```

---

## 📝 Étape 3: Configuration CORS Django

La configuration Django inclut déjà CORS. Vérifiez `backend/settings.py`:

```python
# CORS Configuration (ligne ~220)
CORS_ALLOW_ALL_ORIGINS = True  # ✅ Permet tous les domaines en développement
CORS_ALLOWED_ORIGINS = []

if VERCEL_URL:
    CORS_ALLOWED_ORIGINS.append(f"https://{VERCEL_URL}")
```

**Pour la production, modifiez cela:**

```python
CORS_ALLOWED_ORIGINS = [
    "https://votre-frontend.vercel.app",  # Votre frontend SvelteKit
    "http://localhost:3000",  # Pour le développement local
    "http://localhost:5173",  # Pour Vite dev
]
```

---

## 🚀 Étape 4: Déployer sur Vercel

### Configuration actuelle (vercel.json)

✅ **Déjà configuré pour déployer:**
- Frontend SvelteKit (package.json)
- Backend Django (backend/wsgi.py)
- Réécriture des routes API vers Django

### Processus de déploiement:

1. **Assurez-vous que tout est en git:**
   ```bash
   git add -A
   git commit -m "feat: prepare for Vercel deployment with Django backend"
   git push
   ```

2. **Si vous utilisez le CLI Vercel:**
   ```bash
   vercel deploy --prod
   ```

3. **Ou via le dashboard:**
   - Connectez votre repo GitHub à Vercel
   - Vercel détectera automatiquement `vercel.json`
   - Le build lancera:
     - `npm run build` pour le frontend
     - `collectstatic` pour les fichiers statiques Django
     - Les migrations de base de données

---

## ✅ Checklist de Vérification

### Avant le déploiement local:

- [ ] `.env.local` créé avec `PUBLIC_API_URL="http://localhost:8000"`
- [ ] Django fonctionne: `python backend/manage.py runserver`
- [ ] SvelteKit fonctionne: `npm run dev`
- [ ] API répond: curl `http://localhost:8000/api/geometries/`
- [ ] Frontend se connecte à l'API: ouvrez `http://localhost:5173/app`

### Avant le déploiement sur Vercel:

- [ ] Les objets 3D apparaissent localement
- [ ] Variables d'environnement ajoutées au dashboard Vercel
- [ ] CORS configuré correctement dans `settings.py`
- [ ] `vercel.json` présent et correct
- [ ] `requirements.txt` à jour
- [ ] `SECRET_KEY` définie dans Vercel (ne pas utiliser la clé de demo)

---

## 🐛 Dépannage

### Les objets 3D n'apparaissent pas dans la scène

**Possible causes:**

1. **Django ne démarre pas:**
   ```bash
   cd backend
   python manage.py shell
   ```

2. **L'API retourne une erreur 500:**
   ```bash
   curl -v http://localhost:8000/api/geometries/
   ```

3. **CORS bloque la requête:**
   - Vérifiez la console du navigateur
   - Ajoutez `http://localhost:5173` à `CORS_ALLOWED_ORIGINS`

4. **PUBLIC_API_URL incorrecte:**
   - Vérifiez `.env.local`
   - Redémarrez le serveur Vite après modification

### Erreur: "Cannot find module '@vercel/python'"

```bash
npm install -g vercel
vercel --version
```

---

## 📚 Fichiers à connaître

| Fichier | Rôle |
|---------|------|
| `.env` | Variables de production (Vercel) |
| `.env.local` | Variables de développement local |
| `backend/settings.py` | Configuration Django (CORS, DB, etc.) |
| `vercel.json` | Configuration de déploiement Vercel |
| `src/routes/app/+page.server.js` | Chargement des géométries au serveur |
| `requirements.txt` | Dépendances Python |
| `package.json` | Dépendances Node.js |

---

## 🎉 Résumé

Vous avez maintenant:

1. ✅ `.env.local` pour le développement local
2. ✅ `vercel.json` configuré pour déployer frontend + backend
3. ✅ Django prêt pour Vercel (CORS, DB, etc.)
4. ✅ SvelteKit prêt pour Vercel
5. ✅ Variables d'environnement bien gérées

**Prochaine action:** Testez localement pour vous assurer que tout fonctionne!

```bash
# Terminal 1
cd backend && python manage.py runserver

# Terminal 2
npm run dev
```

Visitez `http://localhost:5173/app` et vous devriez voir vos objets 3D! 🚀
