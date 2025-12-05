# 📋 Diagnostic Complet - Corrections Vercel 500 Errors

## ✅ Corrections Appliquées (Commit: 476dafd)

### 1. **ROOT_URLCONF** [CRITIQUE]
```diff
- ROOT_URLCONF = "urls"
+ ROOT_URLCONF = "backend.urls"
```
**Problème**: Django cherchait `urls.py` à la racine, pas `backend/urls.py`
**Impact**: Django ne trouvait pas les routes API
**Status**: ✅ FIXÉ

### 2. **WSGI_APPLICATION** [CRITIQUE]
```diff
- WSGI_APPLICATION = "wsgi.application"
+ WSGI_APPLICATION = "backend.wsgi.application"
```
**Problème**: Vercel ne trouvait pas le module WSGI
**Impact**: Impossible de démarrer l'app
**Status**: ✅ FIXÉ

### 3. **ALLOWED_HOSTS** [MAJEUR]
```diff
- ALLOWED_HOSTS = ["127.0.0.1", ".vercel.app", "localhost"]
+ ALLOWED_HOSTS = [
+     "127.0.0.1",
+     "localhost",
+     ".vercel.app",
+     "dv-threlte-starter.vercel.app",
+     "*.vercel.app"
+ ]
+ # + Ajouter VERCEL_URL si présent
```
**Problème**: Le domaine specific n'était pas dans la whitelist
**Impact**: Django rejetait les requêtes avec "Bad Host Header" (HTTP 400)
**Status**: ✅ FIXÉ

### 4. **DATABASE CONFIG** [MAJEUR]
```diff
- Neon pooler URL sans gestion appropriée du pool
+ Ajouté:
  - connect_timeout: 10
  - options: statement_timeout=30000
  - CONN_MAX_AGE: 600
  - ATOMIC_REQUESTS: False
```
**Problème**: Vercel Serverless a des connexions éphémères; sans config appropriée, les timeouts causaient 500
**Impact**: Requêtes API échouaient après quelques secondes
**Status**: ✅ FIXÉ

### 5. **LOGGING** [MAJEUR]
```python
# Ajouté config LOGGING complète
- Handlers console et file
- Loggers pour django.db, django.request, Base_threlte_dv
- DEBUG vs INFO selon l'environnement
```
**Problème**: Aucun moyen de voir l'erreur exacte dans Vercel Function Logs
**Impact**: Impossible de diagnostiquer les vrais problèmes
**Status**: ✅ FIXÉ

### 6. **manage.py** [IMPORTANT]
```diff
- os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
+ os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
+ # + Add project root to sys.path
```
**Problème**: manage.py ne trouvait pas settings.py
**Impact**: Impossible d'exécuter des migrations localement
**Status**: ✅ FIXÉ

### 7. **health_check** [UTILE]
```python
# Amélioré pour logger les erreurs
- Simple response
+ logging et messages détaillés
```
**Impact**: Meilleur diagnostic quand health check échoue
**Status**: ✅ FIXÉ

---

## 📊 Plan de Vérification

### Phase 1: Vérification Locale (5-10 minutes)
```bash
# Vérifier que Django démarre localement
python backend/manage.py check --settings=backend.settings

# Démarrer Django
python backend/manage.py runserver 0.0.0.0:8000

# Test health check
curl http://localhost:8000/health/

# Test API
curl http://localhost:8000/api/geometries/
```

### Phase 2: Attendre le déploiement Vercel (3-5 minutes)
- Vercel doit avoir reçu le commit
- Vercel construit le projet
- Vercel déploie automatiquement

### Phase 3: Test sur Vercel Production (2 minutes)
```bash
# Test health check sur Vercel
curl https://dv-threlte-starter.vercel.app/health/

# Vérifier que Django démarre correctement
# Doit retourner:
# {
#   "status": "ok",
#   "database": "✅ Connected",
#   "debug": false,
#   "secret_key_set": true,
#   "allowed_hosts": [...]
# }

# Test API
curl https://dv-threlte-starter.vercel.app/api/geometries/

# Doit retourner des géométries avec code 200
```

### Phase 4: Test Frontend Vercel (1-2 minutes)
```bash
# Naviguer vers https://dv-threlte-starter.vercel.app/app
# Vérifier que la scène 3D charge avec géométries
# Vérifier pas d'erreurs CORS dans console
```

---

## 🔍 Si ça marche pas encore

### Vérifier les logs Vercel:
1. Aller sur https://vercel.com/dvrch/dv-threlte-starter
2. Cliquer sur le dernier déploiement
3. Cliquer sur "Functions" → "api"
4. Lire les logs

### Erreurs possibles restantes:

**Si 500 sur /health/ ou /api/:**
- → Django ne démarre pas encore
- → Vérifier les logs Vercel
- → Chercher "ImportError" ou "ModuleNotFoundError"

**Si 400 (Bad Host Header):**
- → ALLOWED_HOSTS toujours incomplet
- → Ajouter le domaine exact dans settings.py

**Si 403 ou 401:**
- → Problème CSRF ou CORS
- → Mais peu probable en DEBUG=False

**Si pas de géométries:**
- → Django démarre mais DB pas accessible
- → Vérifier DATABASE_URL sur Vercel Dashboard

---

## 🚨 Variables Vercel à Vérifier

Aller sur https://vercel.com/dvrch/dv-threlte-starter/settings/environment-variables

Vérifier que ces variables existent:
- ✅ `DEBUG=False`
- ✅ `SECRET_KEY=django-insecure-...`
- ✅ `DATABASE_URL=postgresql://...`
- ✅ `BLOB_READ_WRITE_TOKEN=vercel_blob_...`

---

## ✨ Prochaines Étapes

1. **Attendre ~5 minutes** que Vercel finisse le build
2. **Tester /health/** sur Vercel
3. Si 200 → health check marche
4. Tester **/api/geometries/** 
5. Si 200 → API marche
6. Visiter **/app** et vérifier la 3D scene

**Status: En attente de redéploiement Vercel** ⏳

