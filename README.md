# Pocket Ledger Backend

Backend API cho Pocket Ledger, xay dung bang FastAPI, SQLAlchemy, Pydantic v2 va PostgreSQL.

## Main Docs

- Architecture: `ARCHITECTURE.md`
- Project structure: `PROJECT_STRUCTURE.md`
- Environment setup: `ENV_SETUP.md`
- Root API contract: `../docs/api-contract.md`
- Analytics task: `../docs/TASK_ANALYTICS_APP_SHELL.md`
- Transaction summary task: `../docs/TASK_TRANSACTION_SUMMARY.md`

## Runtime Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic v2
- JWT Bearer auth
- passlib bcrypt

## Routers

- `GET /health`
- `POST /auth/token`
- `/users`: admin-only user management.
- `/transactions`: transaction CRUD, summaries and analytics.
- `/categories`: category metadata.

## Transaction Analytics Endpoints

All endpoints require:

```http
Authorization: Bearer <access_token>
```

Permission behavior:

- Normal user aggregates only own transactions.
- Admin aggregates all transactions visible by current admin behavior.

Endpoints:

- `GET /transactions/analytics/overview`
- `GET /transactions/analytics/by-category`
- `GET /transactions/analytics/timeseries`

Common filters:

- `date_from`: required `YYYY-MM-DD`, inclusive.
- `date_to`: required `YYYY-MM-DD`, inclusive.
- `transaction_type`: optional `income` or `expense`.
- `category_key`: optional category filter. If omitted, all categories are included.

Timeseries also supports:

- `group_by`: optional `day`, `week`, or `month`; default `day`.

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` using `ENV_SETUP.md`.

Run:

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload
```

Swagger UI:

```text
http://localhost:8001/docs
```

## Ports

- Local direct run: `8001`.
- Docker compose exposed port: `5001`.

## Database Note

`fact_transactions.id` uses `uuid_generate_v4()`, so PostgreSQL needs:

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```
