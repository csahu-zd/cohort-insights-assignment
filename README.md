# Cohort Insights API

A FastAPI service that saves text documents in MongoDB, processes them through a two-stage background pipeline, and uses Redis for rate limits and cached results.

## What you get

- Document submission, status polling, updates, and user-scoped listing.
- A background flow: `queued → processing → enriching → completed` (or `failed`).
- Redis caching for completed content and active-job limits per user.
- Swagger UI for trying endpoints and RedisInsight for viewing Redis keys.

## Run with Docker

Run these commands from the project directory:

```powershell
docker compose up -d --build
docker compose ps
```

Open:

- Swagger: http://localhost:8000/docs
- Health: http://localhost:8000/health
- RedisInsight: http://localhost:5540
- MongoDB Compass: `mongodb://127.0.0.1:27018/?directConnection=true`

In RedisInsight, add `redis://redis:6379` to view the application’s Redis database.

To follow API logs or stop the services:

```powershell
docker compose logs -f api
docker compose down
```

For local test runs, install the same single dependency set and run pytest:

```powershell
pip install -r requirements.txt
pytest
```

## API endpoints

All document requests require the `X-User-Id` header.

| Method | Endpoint | Use |
|---|---|---|
| `GET` | `/health` | Checks whether MongoDB and Redis are reachable. |
| `POST` | `/documents` | Creates a document and queues it for processing; repeated content may return a cached result. |
| `GET` | `/documents/{document_id}` | Gets one of your documents and its processing-stage status. |
| `PATCH` | `/documents/{document_id}` | Replaces document content and queues both stages again. |
| `GET` | `/users/{user_id}/documents` | Lists your documents; supports `page`, `page_size`, and `status`. |
| `GET` | `/documents/by-ref/{client_doc_ref}` | Finds your document using an external partner reference. |

## Project structure

```text
app/
  api/          Routes and request dependencies
  core/         Environment configuration and logging
  db/           MongoDB and Redis connections
  schemas/      Request and response models
  services/     Document operations and Redis helpers
  workers/      Background processing stages
  main.py       FastAPI app and startup/shutdown
tests/          API integration tests
```
