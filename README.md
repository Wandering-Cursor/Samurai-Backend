# Samurai-Backend

## About

# TODO:
- [ ] Add a proper description
- [ ] Recreate CI/CD workflow
- [ ] Add docker file for backend

## Installation

For this project we need:
- [Python 3.12 (or newer)](https://www.python.org/)
- [PDM](https://pdm-project.org/latest/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Setup

1. Clone the repository
1. Install the dependencies
1. Start the compose files
1. Create `*.env` files
1. Run the migrations
1. Create administrator user
1. Use the API

### 1. Clone the repository

```bash
# HTTPS
git clone https://github.com/Wandering-Cursor/Samurai-Backend.git
# OR SSH
git clone git@github.com:Wandering-Cursor/Samurai-Backend.git
# OR GitHub CLI
gh repo clone Wandering-Cursor/Samurai-Backend
```

### 2. Install the dependencies

All the dependencies are managed by PDM, so you just need to:
1. Install PDM
2. Install the dependencies

#### 2.1. Install PDM

You can refer to [PDM Docs](https://pdm-project.org/latest/#recommended-installation-method) on that matter

#### 2.2. Install the dependencies

```bash
pdm install
```

### 3. Start the compose files

```bash
docker compose -f compose/dev-docker-compose.yml up -d
```

This will start the database and the redis server.

### 4. Create `*env` secrets

This project needs two `.env` files:
- `security_env` - Handles the security settings (JWT, CORS, etc.)
- `settings_env` - Handles general settings (Debug mode, DB connection, etc.)

Examples are provided in [security.env.md](./security.env.md) and [settings.env.md](./settings.env.md)
You can also refer to [settings models](./src/samurai_backend/settings.py) for more details
They should be placed in `/run/secrets/` folder. (Unless you are running Docker. Then you should use `./compose/.secrets/` folder.)

### 5. Run the migrations

To run migrations you have to be in: `src/samurai_backend/` folder.
```bash
## Assuming you are in the root of the project

cd src/samurai_backend/

alembic upgrade head
```

For more information on alembic migrations (creation, reversal, applying), you can refer to CLI docs, or [Alembic Docs](https://alembic.sqlalchemy.org/en/latest/)
```bash
alembic --help
```

### 6. Create administrator user

Creating an administrator user is done through the CLI.
```bash
pdm create_admin
```

Then follow prompts to create the user.

### 7. Use the API

Start the api with your editor (there's a launch configuration for VSCode) or with the following command:
```bash
pdm run_server
```

P.S. You can also use any other configuration for the server, like `gunicorn`, `uvicorn`, etc.
The app is invoked through `samurai_backend.app:app` module.
