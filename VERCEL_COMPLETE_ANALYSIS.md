# 🎯 Analyse Complète & Corrections des 500 Errors Vercel

## 📍 Situation Initiale

**Problème**: Déploiement Vercel retourne **500 (FUNCTION_INVOCATION_FAILED)** sur tous les endpoints Django:
- `GET /health/` → 500 ❌
- `GET /api/geometries/` → 500 ❌
- `GET /api/types/` → 500 ❌

**Local**: ✅ Tout fonctionne parfaitement avec `http://localhost:8000`

---

## 🔍 Analyse des 5 Causes Principales

### **Cause 1: ROOT_URLCONF Incorrect [CRITIQUE]**

**Le Problème:**
```python
# backend/settings.py (AVANT)
ROOT_URLCONF = "urls"
```

Django cherchait `/urls.py` à la **racine du projet**, pas `/backend/urls.py`

**Pourquoi ça marche localement?**
- Localement, vous exécutez depuis `/backend/` donc Django la trouve

**Pourquoi ça échoue sur Vercel?**
- Vercel exécute depuis **la racine du projet** (`/`)
- Django ne trouve pas `/urls.py` → ImportError → 500

**La Correction:**
```python
# backend/settings.py (APRÈS)
ROOT_URLCONF = "backend.urls"
```

---

### **Cause 2: WSGI_APPLICATION Incorrect [CRITIQUE]**

**Le Problème:**
```python
# backend/settings.py (AVANT)
WSGI_APPLICATION = "wsgi.application"
```

Même problème que #1 - Django cherche `/wsgi.py`, pas `/backend/wsgi.py`

**La Correction:**
```python
# backend/settings.py (APRÈS)
WSGI_APPLICATION = "backend.wsgi.application"
```

---

### **Cause 3: ALLOWED_HOSTS Incomplet [MAJEUR]**

**Le Problème:**
```python
# AVANT
ALLOWED_HOSTS = ["127.0.0.1", ".vercel.app", "localhost"]
```

Django recevait:
```
Host: dv-threlte-starter.vercel.app
```

Mais votre config disait:
- ✅ Autoriser `.vercel.app` (wildcard)
- ❌ Mais Django est strict! Wildcard incomplet

Django rejetait → **400 Bad Host Header**

**La Correction:**
```python
# APRÈS
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    ".vercel.app",
    "dv-threlte-starter.vercel.app",  # ← Domaine exact
    "*.vercel.app"
]

# + Dynamic VERCEL_URL from Vercel env
VERCEL_URL = os.environ.get("VERCEL_URL")
if VERCEL_URL and VERCEL_URL not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.insert(0, VERCEL_URL)
```

---

### **Cause 4: DATABASE Configuration Inadaptée à Serverless [MAJEUR]**

**Le Problème:**
```python
# AVANT
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://...@...neon.tech/neondb"
)
db_config = dj_database_url.parse(DATABASE_URL)
db_config['OPTIONS'].update({
    'sslmode': 'require',
    'connect_timeout': 10,
})
```

**Pourquoi ça échoue sur Vercel?**
- Vercel est **serverless** = fonctions éphémères
- Chaque requête crée une NOUVELLE fonction
- Chaque fonction OUVRE une nouvelle connexion DB
- Sans pool config appropriée = **timeouts fréquents**
- Neon DB a des limites de connexions strictes

**La Correction:**
```python
# APRÈS
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://...@...neon.tech/neondb?sslmode=require"
)

db_config = dj_database_url.parse(DATABASE_URL)
if 'OPTIONS' not in db_config:
    db_config['OPTIONS'] = {}

db_config['OPTIONS'].update({
    'sslmode': 'require',
    'connect_timeout': 10,
    'options': '-c statement_timeout=30000'  # 30 sec timeout
})

DATABASES = {"default": db_config}

if DATABASE_URL and 'neon' in DATABASE_URL:
    DATABASES['default']['CONN_MAX_AGE'] = 600  # Reuse connections
    DATABASES['default']['ATOMIC_REQUESTS'] = False  # Don't lock all requests
```

---

### **Cause 5: Pas de Logging Vercel [MAJEUR]**

**Le Problème:**
- Quand ça retourne 500, Django cache l'erreur réelle
- Aucun moyen de voir la cause dans les logs

**La Correction:**
```python
# Ajouté dans settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'WARNING',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
        'Base_threlte_dv': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

Maintenant vous voyez les erreurs dans **Vercel Function Logs**!

---

## 🔧 Autres Corrections

### **manage.py: DJANGO_SETTINGS_MODULE**
```python
# AVANT
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

# APRÈS
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
```

### **health_check endpoint: Logging amélioré**
```python
# Ajouté logging pour diagnostiquer les problèmes
def health_check(request):
    response_data = {
        "status": "ok",
        "debug": settings.DEBUG,
        "secret_key_set": bool(settings.SECRET_KEY),
        "allowed_hosts": settings.ALLOWED_HOSTS,
    }
    
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        response_data["database"] = "✅ Connected"
        logger.info("Health check: Database connected")
    except Exception as e:
        response_data["database"] = f"❌ Error: {str(e)}"
        logger.error(f"Health check failed: {str(e)}")
    
    return JsonResponse(response_data)
```

---

## 📋 Résumé des Changements

| Fichier | Changement | Cause | Impact |
|---------|-----------|-------|---------|
| `backend/settings.py` | `ROOT_URLCONF = "backend.urls"` | Django ne trouvait pas urls.py | CRITIQUE |
| `backend/settings.py` | `WSGI_APPLICATION = "backend.wsgi.application"` | Django ne trouvait pas wsgi.py | CRITIQUE |
| `backend/settings.py` | Ajout de `dv-threlte-starter.vercel.app` à ALLOWED_HOSTS | Django rejetait le domaine | MAJEUR |
| `backend/settings.py` | Améliorations DATABASE avec pool config | Timeouts DB sur Vercel | MAJEUR |
| `backend/settings.py` | Config LOGGING complète | Aucun diagnostic possible | MAJEUR |
| `backend/manage.py` | `DJANGO_SETTINGS_MODULE = 'backend.settings'` | manage.py ne trouvait pas settings | IMPORTANT |
| `backend/urls.py` | Logging dans health_check | Pas de diagnostic | UTILE |

---

## ✅ Vérification Après Corrections

### Phase 1: Local (5-10 min)
```bash
# Vérifier Django démarre
python -m django check --settings=backend.settings

# Démarrer le serveur
python backend/manage.py runserver 0.0.0.0:8000

# Tester health check
curl http://localhost:8000/health/
# Doit retourner 200 + JSON avec "database": "✅ Connected"

# Tester API
curl http://localhost:8000/api/geometries/
# Doit retourner 200 + liste des géométries
```

### Phase 2: Attendre Vercel (3-5 min)
- Vercel reçoit le commit
- Vercel reconstruit
- Vercel redéploie

### Phase 3: Production Vercel (2-5 min)
```bash
# Tester health check Vercel
curl https://dv-threlte-starter.vercel.app/health/

# Doit retourner:
# {
#   "status": "ok",
#   "database": "✅ Connected",
#   "debug": false,
#   "secret_key_set": true,
#   "allowed_hosts": [...]
# }

# Tester API Vercel
curl https://dv-threlte-starter.vercel.app/api/geometries/

# Doit retourner 200 + géométries
```

### Phase 4: Frontend (1-2 min)
```bash
# Naviguer vers:
# https://dv-threlte-starter.vercel.app/app

# Vérifier:
# ✅ Page charge sans erreur
# ✅ 3D scene s'affiche
# ✅ Géométries apparaissent
# ✅ Pas d'erreurs CORS en console
# ✅ Console affiche "✅ Loaded geometries: 61"
```

---

## 🚀 Status Actuel

**Commit**: `476dafd` poussé vers `origin/master`

**Attendant**: ⏳ Redéploiement Vercel (3-5 minutes)

**Prochaine étape**: Attendre puis tester `/health/` endpoint

---

## 📚 Ressources

- **Vercel Django Docs**: https://vercel.com/docs/functions/serverless-functions/runtimes/python
- **Django Deployment Checklist**: https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
- **Neon Connection Pooling**: https://neon.tech/docs/connect/connection-pooling
- **Django ALLOWED_HOSTS**: https://docs.djangoproject.com/en/5.0/ref/settings/#allowed-hosts

