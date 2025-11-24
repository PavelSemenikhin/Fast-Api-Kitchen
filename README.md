# FastAPI Project Template (with Local & Docker Environments)

A clean, production-ready FastAPI template using:
- async SQLAlchemy
- Alembic migrations (LOCAL)
- Docker Compose (runtime)
- Two environment modes (`.env.local` & `.env.docker`)
- Modular project layout  
Perfect for starting any new FastAPI project.

GitHub repository: https://github.com/PavelSemenikhin/Fast-Api-App.git

---

# 1. Clone the Repository

```
git clone https://github.com/PavelSemenikhin/Fast-Api-App.git
cd Fast-Api-App
```

Project structure:

```
.
├── src/                 # All application code
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

# 2. Environment Configuration (IMPORTANT)

This template uses **two separate environment files**:

| File | Purpose | DB Host |
|------|----------|----------|
| `.env.local` | Local development + Alembic migrations | `localhost` |
| `.env.docker` | Docker runtime | `pg` |

Inside `/src`, create:

```
cp src/.env.local.sample src/.env.local
cp src/.env.docker.sample src/.env.docker
```

---

# 3. Environment Files Content

## `.env.local` (LOCAL mode — for Alembic & IDE runs)

```
APP_CONFIG__DB__URL=postgresql+asyncpg://postgres:password@localhost:5432/postgres
APP_CONFIG__DB__ECHO=1
```

## `.env.docker` (DOCKER mode — container-to-container)

```
APP_CONFIG__DB__URL=postgresql+asyncpg://postgres:password@pg:5432/postgres
APP_CONFIG__DB__ECHO=0
```

---

# 4. Install Dependencies Locally (without Docker)

```
pip install poetry
poetry install
```

This installs all Python dependencies for local development & migrations.

---

# 5. Running Alembic Migrations (LOCAL ONLY)

Alembic **must be executed locally**, not inside Docker.

Before running any Alembic command, load `.env.local`:


## Windows PowerShell - every time you open a new.

```
cd src

Get-Content .env.local | Foreach-Object {
    if ($_ -match "^(?<name>[^=]+)=(?<value>.*)$") {
        Set-Item -Path "Env:\$($matches['name'])" -Value $($matches['value'])
    }
}
```

---

## Create a new migration

```
alembic revision --autogenerate -m "init"
```

## Apply migrations

```
alembic upgrade head
```

---


---

# 6. Run FastAPI with Docker

Docker automatically uses `.env.docker`:

```
docker compose up --build
```

Application is available at:

```
http://localhost:8000
```

To stop containers:

```
docker compose down
```

---

# 8. Project Structure

```
src/
│
├── api/
│   ├── api_v1/
│   └── router.py
│
├── core/
│   ├── config.py
│   └── models/
│
├── crud/
├── schemas/
├── migrations/       # Alembic migrations
├── db_helper.py
└── main.py
```

---

# 9. Optionally: Run Alembic inside Docker

Not recommended, but possible:

```
docker compose exec app alembic upgrade head 
```

---

# 10. Recommended Workflow

1. Clone repo  
2. Create `.env.local` & `.env.docker` from `.env.sample`  
3. Run PostgreSQL via Docker  
4. Run Alembic migrations locally (`localhost`)  
5. Start FastAPI through Docker (`pg` hostname)  
6. Develop normally  
7. Create migrations when models change  
8. Redeploy with Docker  

This matches how senior backend engineers structure FastAPI + SQLAlchemy projects.

---

You're ready to build production-grade FastAPI applications 🚀
