# Screenshot App

Traitement de captures d'écran en temps réel : upload, stockage, notifications live.

Projet réalisé pendant mon stage DevOps Full-Stack chez Free Iliad, comme test d'architecture (queues, websockets, stockage S3-like).

## Fonctionnalités

- Upload de captures d'écran
- Traitement asynchrone via queue (worker Python)
- Notifications temps réel (WebSockets)
- Stockage des fichiers (MinIO / S3)

## Stack

- Backend : Laravel (PHP)
- Frontend : Vue.js
- Worker : Python
- Queue : Redis
- Websockets : Soketi
- Stockage : MinIO (S3-compatible)
- DB : PostgreSQL
- Reverse proxy : nginx
- CI/CD : GitLab CI, build + push des images vers le Container Registry (déclenchement manuel)

## Architecture

Le repo build 4 images distinctes (nginx, vue, laravel/PHP — réutilisée pour laravel et laravel-worker —, et worker Python), orchestrées avec nginx en entrée. Laravel garde `ShouldBroadcast` avec queue (au lieu d'un broadcast direct), pour rester proche d'un vrai fonctionnement de prod.

```
Client → nginx (4242)
           ├── /        → vue
           ├── /api     → laravel
           ├── /storage → minio
           └── /app     → soketi (websockets)

laravel → redis (queue) → laravel-worker (queue Laravel)
                        → worker (Python, traitement des screenshots)
```

## Déploiement

Le pipeline `.gitlab-ci.yml` de ce repo build les 4 images et les push vers le Container Registry (GitLab local), avec un tag de version et `latest`. Déclenchement manuel, sur la branche `main`.

Le déploiement à proprement parler se fait depuis le pipeline du repo [screenshot-app_prod](https://github.com/Tenmazzz/screenshot-app_prod) : il copie `.env` et le `docker-compose` correspondant par SCP vers une VM (VirtualBox, exposée via tunnel Cloudflare), puis se connecte en SSH pour pull les images, relancer les conteneurs et lancer les migrations Laravel. Deux jobs manuels séparés : un pour la branche `staging`, un pour `main` (prod).

## Installation (dev)

Prérequis : Docker + Docker Compose

```bash
git clone https://github.com/Tenmazzz/screenshot-app.git
cd screenshot-app
cp backend/.env.example backend/.env
docker compose -f docker-compose.dev.yml up --build
```

App accessible sur `http://localhost:4242`.

> Un `docker-compose.prod.yml` existe aussi pour tout lancer depuis ce repo en une fois, mais il n'est plus maintenu à jour — pas garanti qu'il fonctionne.

### .env (backend)

Le `.env.example` fourni par Laravel n'est pas à jour avec la stack Docker (il référence MySQL au lieu de PostgreSQL). Adapter au minimum :

```env
DB_CONNECTION=pgsql
DB_HOST=postgres
DB_PORT=5432
DB_DATABASE=screenshot_app
DB_USERNAME=screnshoot_user
DB_PASSWORD=password123!

REDIS_HOST=redis
REDIS_PORT=6379

QUEUE_CONNECTION=redis
BROADCAST_DRIVER=redis
```

> Les identifiants postgres/MinIO ci-dessus sont ceux définis en dur dans `docker-compose.dev.yml`, à changer avant tout déploiement réel.

### Services

| Service | Rôle | Port |
|---|---|---|
| nginx | reverse proxy (point d'entrée) | 4242 |
| vue | frontend | 8080 |
| laravel | backend API | via nginx |
| laravel-worker | queue Laravel (broadcast) | - |
| worker | traitement Python des screenshots | - |
| redis | queue | 6379 |
| postgres | DB | 5432 |
| minio | stockage S3 | 9000 / 9001 (console) |
| soketi | websockets | 6001 |

MinIO utilise des identifiants par défaut (`minioadmin` / `minioadmin`) définis dans le compose, à changer en prod.

## Structure

```
.
├── backend
│   ├── app
│   ├── config
│   ├── routes
│   └── .env.example
├── frontend
│   └── src
├── worker
│   └── worker.py
├── docker
│   ├── nginx
│   ├── php
│   ├── vue
│   └── worker
├── docker-compose.dev.yml
├── docker-compose.prod.yml   # non maintenu
└── .gitlab-ci.yml