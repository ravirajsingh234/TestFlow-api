# TestFlow-api

FastAPI microservice with PostgreSQL and Redis, Docker Compose, health checks, multi-stage builds, and non-root container execution.

## Overview

This repository contains a FastAPI service that stores tasks in PostgreSQL and caches task data in Redis.

The application is packaged using a multi-stage Docker build and can be run locally with Docker Compose.

## Contents

- `Dockerfile` — builds the FastAPI app image using a Python virtual environment.
- `docker-compose.yml` — defines `api`, `postgres`, and `redis` services.
- `app/` — FastAPI application code, including models, schemas, database connectivity, and Redis helper code.
- `requirements.txt` — Python dependencies for the app.

## Setup

1. Install Docker Desktop.
2. Configure your Postgres credentials for Docker Compose.

3. Build and run with Docker Compose:

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000`.

## Docker-only run

To run the app image directly without Compose, build the image and configure your runtime environment variables separately.

> Note: direct Docker run requires a running PostgreSQL instance accessible from the container.

## Architecture

See `ARCHITECTURE.md` for a diagram and component relationships.

## Notes

- `app/main.py` creates the database schema at startup using SQLAlchemy metadata.
- `app/database.py` uses environment variables to build the Postgres connection URL.
- `app/models.py` defines the `Task` model, and `app/schemas.py` defines Pydantic request/response models.
