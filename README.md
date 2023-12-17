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

4. Fill the file according to the example.env file

5. Run the project
```bash
docker compose up -d --build
```

6. Create a superuser
```bash
docker compose exec web python DiplomaPulse/manage.py createsuperuser
```

