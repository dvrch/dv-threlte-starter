#!/bin/bash
# 🎉 Résumé de la configuration complète

cat << 'EOF'

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃        🚀 CONFIGURATION COMPLÈTE FINALISÉE 🚀             ┃
┃    Django Backend + SvelteKit Frontend sur Vercel       ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

✅ ÉTAPES COMPLÉTÉES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. ✓ .env.local créé
   └─ PUBLIC_API_URL="http://localhost:8000" (développement)

2. ✓ Django configuré
   └─ CORS support localhost:5173
   └─ Database Neon PostgreSQL
   └─ Vercel Blob Storage

3. ✓ SvelteKit configuré
   └─ Récupère PUBLIC_API_URL depuis .env.local
   └─ Affiche objets 3D depuis l'API Django

4. ✓ Vercel.json optimal
   └─ Frontend: SvelteKit static build
   └─ Backend: Django Python WSGI
   └─ API routes: /api/* → Django

5. ✓ Scripts de démarrage
   └─ start-dev.sh (automatisé)
   └─ bash dev.sh (manuel)

6. ✓ Python environment
   └─ .venv/bin/python configuré
   └─ Django, DRF, CORS installés

7. ✓ Migrations Django
   └─ Base de données prête

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 LANCER LE DÉVELOPPEMENT LOCAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Méthode 1 - Automatisée (RECOMMANDÉE):
  $ cd /home/kd/Bureau/dv-threlte-starter
  $ chmod +x start-dev.sh
  $ ./start-dev.sh

  ↓
  ✅ Django lancé sur http://localhost:8000
  ✅ SvelteKit lancé sur http://localhost:5173
  ✅ Ouvrir http://localhost:5173/app

Méthode 2 - Manuelle (2 terminaux):

  Terminal 1 - Backend:
  $ cd backend
  $ /home/kd/Bureau/dv-threlte-starter/.venv/bin/python manage.py runserver

  Terminal 2 - Frontend:
  $ npm run dev
  $ # Ouvrir http://localhost:5173

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ VÉRIFICATIONS À FAIRE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. API Django fonctionne:
   $ curl http://localhost:8000/api/geometries/
   
   Attendu: JSON avec liste des géométries (peut être vide)

2. Frontend se connecte:
   Ouvrir http://localhost:5173/app
   
   Attendu: Scène 3D avec objets si la base de données en contient

3. CORS fonctionne:
   Vérifier console du navigateur (F12)
   
   ❌ Ne pas voir d'erreur "CORS blocked"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌐 DÉPLOYER SUR VERCEL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Étape 1 - Ajouter Variables d'Environnement:
  1. Ouvrir https://vercel.com/dashboard
  2. Sélectionner votre projet
  3. Settings > Environment Variables
  4. Ajouter:
     
     PUBLIC_API_URL=https://dv-threlte-starter.vercel.app
     PUBLIC_STATIC_URL=https://w0cb58ft2bj7sg0v.public.blob.vercel-storage.com
     DEBUG=False
     SECRET_KEY=<votre-clé-de-production>
     BLOB_READ_WRITE_TOKEN=<token-vercel>
     STORE_ID=store_W0CB58Ft2bj7Sg0v

Étape 2 - Déployer:
  $ git add -A
  $ git commit -m "Deploy: full Django + SvelteKit setup"
  $ git push origin master
  
  Vercel détectera vercel.json et déploiera automatiquement!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 STRUCTURE IMPORTANTE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/home/kd/Bureau/dv-threlte-starter/
├─ .env                    ← Production (PUBLIC_API_URL pour Vercel)
├─ .env.local              ← Développement (localhost:8000)
├─ .env.production         ← Notes pour Vercel
├─ vercel.json             ← Configuration Vercel (frontend + backend)
├─ requirements.txt        ← Dépendances Python
├─ package.json            ← Dépendances Node.js
├─ start-dev.sh            ← Script lancer tout
├─ build-vercel.sh         ← Script post-build Vercel
│
├─ backend/
│  ├─ settings.py          ← CORS + Database + Blob configurés
│  ├─ wsgi.py              ← Point d'entrée WSGI
│  ├─ manage.py
│  └─ ...
│
├─ src/
│  └─ routes/app/
│     ├─ +page.server.js   ← Récupère geometries depuis API
│     └─ +page.svelte      ← Affiche scène 3D
└─ ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🐛 DÉPANNAGE RAPIDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Problème: "Cannot GET /api/geometries/"
Solution: S'assurer que Django démarre bien
  $ cd backend
  $ /home/kd/Bureau/dv-threlte-starter/.venv/bin/python manage.py runserver

Problème: "CORS error" dans la console
Solution: Vérifier backend/settings.py ligne ~220
  S'assurer que http://localhost:5173 est dans CORS_ALLOWED_ORIGINS

Problème: "PUBLIC_API_URL not configured"
Solution: Vérifier .env.local existe
  $ cat .env.local | grep PUBLIC_API_URL

Problème: "Objects 3D ne s'affichent pas en production"
Solution: Vérifier la variable PUBLIC_API_URL dans Vercel Dashboard
  Doit pointer vers votre API Django publique (pas localhost!)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 DOCUMENTATION COMPLÈTE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ouvrir: DEPLOYMENT_GUIDE_COMPLETE.md
  $ cat DEPLOYMENT_GUIDE_COMPLETE.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ VOUS ÊTES PRÊT! 
🚀 Lancez: ./start-dev.sh
👀 Regardez: http://localhost:5173/app

┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

EOF
