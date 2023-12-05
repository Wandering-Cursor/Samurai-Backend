# Outline of the project

## Introduction
This project is a backend part of the project.
It consists of the following parts:
 - Django Application (DiplomaPulse)
 - Database (PostgreSQL)
 - Cache (Redis)
 - Task processing (Celery)
 - Message broker (Redis)
 - Web server (Nginx + Gunicorn)

## Installation
### Requirements
 - Git
 - Docker
 - Docker-compose

### Installation
1. Clone the repository
```bash
git clone *link*
```

2. Go to the project directory
```bash
cd *Repository Name*
```

3. Create a file with environment variables
```bash
touch .env
```

4. Fill the file with the following variables
```bash
SECRET_KEY=*secret key*
DEBUG=*debug mode*
ALLOWED_HOSTS=*allowed hosts*
DB_NAME=*database name*
DB_USER=*database user*
DB_PASSWORD=*database password*
DB_HOST=db
DB_PORT=5432
REDIS_HOST=redis
REDIS_PORT=6379
EMAIL_HOST=*email host*
EMAIL_PORT=*email port*
EMAIL_HOST_USER=*email host user*
EMAIL_HOST_PASSWORD=*email host password*
EMAIL_USE_TLS=*email use tls*
EMAIL_USE_SSL=*email use ssl*
```

5. Run the project
```bash
docker compose up -d --build
```

6. Create a superuser
```bash
docker compose exec web python DiplomaPulse/manage.py createsuperuser
```

