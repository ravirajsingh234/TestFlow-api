# Architecture Diagram

This document describes the main components and how they interact in the `TestFlow-api` project.

```text
+-----------------+        +------------------+        +----------------+
|                 |        |                  |        |                |
|   User / API    | <----> |   FastAPI App    | <----> |   PostgreSQL   |
|   Client        |        |   (app/main.py)  |        |   (postgres)   |
|                 |        |                  |        |                |
+-----------------+        +------------------+        +----------------+
                                     |
                                     |
                                     v
                              +------------------+
                              |                  |
                              |      Redis       |
                              |   (redis cache)  |
                              |                  |
                              +------------------+
```

## Components

- **FastAPI App**: Serves REST endpoints and loads schema definitions.
- **PostgreSQL**: Stores persistent task data.
- **Redis**: Caches task query results to reduce repeated database load.
- **Docker Compose**: Orchestrates service startup and shared networking.

## Data flow

1. Client sends request to FastAPI.
2. FastAPI routes requests through endpoints in `app/main.py`.
3. The app uses `app/database.py` to open a SQLAlchemy session connected to Postgres.
4. The app uses `app/redis_client.py` to check and update Redis cache.
5. Responses are returned to the client.

## Deployment

- `api` service runs the FastAPI application.
- `postgres` service hosts the database.
- `redis` service hosts the cache.

Use `docker compose up --build` to launch all services together.
