# Studio Ghibli Users API

A FastAPI application that manages users and lets authenticated users retrieve Studio Ghibli API data according to their role.

## Features

- Create, list, retrieve, update, and delete users
- Admin login with bearer-token authentication
- Hashed passwords and role-based access
- Ghibli collection and item lookups
- PostgreSQL persistence
- Docker Compose startup

## Roles

| Role | Ghibli data access |
|---|---|
| `admin` | All collections |
| `films` | Films |
| `people` | People |
| `locations` | Locations |
| `species` | Species |
| `vehicles` | Vehicles |

Only an authenticated admin can manage users. A resource-role user can retrieve only the matching Ghibli collection.

## Requirements

- Docker Desktop with Docker Compose
- Git

## First-time setup

1. Clone this repository and enter its directory.
2. Create a local environment file:

   ```bash
   cp .env.example .env
   ```

3. Fill in the values in `.env`. Generate a JWT secret with:

   ```bash
   openssl rand -hex 32
   ```

   Use a separate generated value for `POSTGRES_PASSWORD`. Do not commit `.env`.

4. Start the API and database:

   ```bash
   docker compose up --build
   ```

   Compose waits for PostgreSQL to become healthy. The API container runs Alembic migrations, then starts FastAPI. On first startup, the app creates the admin account from the configured environment values.

5. Open the interactive API docs at <http://127.0.0.1:8000/docs>.

## Authentication

Use **Authorize** in `/docs` and enter the admin username and password. The token endpoint is:

```text
POST /api/v1/auth/token
```

It accepts form fields named `username` and `password`. Authenticated requests use a bearer token.

## User endpoints

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/api/v1/users/` | Admin creates a user |
| `GET` | `/api/v1/users/` | Admin lists users |
| `GET` | `/api/v1/users/{user_id}` | Admin retrieves a user |
| `PUT` | `/api/v1/users/{user_id}` | Admin updates a user |
| `DELETE` | `/api/v1/users/{user_id}` | Admin deletes a user |
| `PUT` | `/api/v1/auth/password` | Authenticated user changes their password |

Example user creation body:

```json
{
  "name": "Films Reader",
  "username": "films-reader",
  "password": "replace-with-a-strong-password",
  "role": "films"
}
```

## Ghibli endpoints

A logged-in user can retrieve their permitted collection:

```text
GET /api/v1/ghibli/{resource}
GET /api/v1/ghibli/{resource}/{item_id}
```

Allowed resource names are `films`, `people`, `locations`, `species`, and `vehicles`. Admin users can request any resource.

## Stopping the app

Stop the foreground Compose process with **Ctrl+C**, or run:

```bash
docker compose down
```

The PostgreSQL volume remains so the data persists. To intentionally erase the local database, use `docker compose down -v`.

## Configuration

Copy `.env.example` to `.env` and provide the PostgreSQL credentials, admin credentials, JWT secret, and token expiration setting. Keep real secrets out of Git.