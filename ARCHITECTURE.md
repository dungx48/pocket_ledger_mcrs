# Backend Architecture

Pocket Ledger backend follows a layered FastAPI architecture.

## Layers

- `controller`: HTTP route definitions and dependency wiring.
- `service`: business logic and permission checks.
- `repository`: SQLAlchemy database queries.
- `model`: ORM table definitions.
- `schemas.py`: Pydantic request/response schemas.
- `utils`: config, database and security helpers.
- `middleware`: request logging.

Entry point: `src/main.py`.

## Runtime Components

- FastAPI app in `src/main.py`.
- SQLAlchemy engine/session in `src/utils/database.py`.
- PostgreSQL stores users, transactions and categories.
- JWT auth via `src/utils/security.py`.
- `SafeLoggingMiddleware` logs request timing.

## Request Flow

```text
HTTP request
  -> FastAPI router/controller
  -> service
  -> repository
  -> SQLAlchemy Session
  -> PostgreSQL
  -> Pydantic response
```

## Auth And Permission

- Login endpoint: `POST /auth/token`.
- Protected endpoints use `Depends(get_current_user)`.
- Token payload contains `sub=username` and `exp`.
- `/users` endpoints require admin.
- `/transactions` endpoints:
  - Admin can access all transactions according to current behavior.
  - Normal user can access only own transactions.
- Analytics endpoints use the same transaction visibility rules.

## Data Model

### `fact_users`

- `id`
- `username`
- `hashed_password`
- `fullname`
- `is_admin`

### `fact_transactions`

- `id`
- `user_id`
- `category_key`
- `amount`
- `date`
- `note`
- `transaction_type`
- `created_at`

Indexes:

- `(user_id, date)`
- `category_key`

### `dim_categories`

- `id`
- `description`
- `key`
- `value`
- `is_active`
- `table_name`
- `field_name`

## Transaction Controller

File: `src/controller/transaction_controller.py`.

Current endpoint groups:

- Transaction list and CRUD.
- Monthly and weekly summary.
- Analytics overview, by-category and timeseries.

## Transaction Analytics

Analytics endpoints are under:

```text
/transactions/analytics
```

Endpoints:

- `GET /transactions/analytics/overview`
- `GET /transactions/analytics/by-category`
- `GET /transactions/analytics/timeseries`

Common validation:

- `date_from` and `date_to` are required.
- `date_to >= date_from`.
- Invalid date range returns `400`.
- Invalid `transaction_type` returns `400`.

Supported filters:

- `transaction_type`: optional `income` or `expense`.
- `category_key`: optional category filter.

Timeseries supports:

- `group_by=day`
- `group_by=week`
- `group_by=month`

## Transaction Repository

File: `src/repository/transaction_repository.py`.

Important methods:

- `list(...)`
- `monthly_summary(...)`
- `weekly_summary(...)`
- `analytics_overview(...)`
- `analytics_by_category(...)`
- `analytics_timeseries(...)`

Shared read filters are applied through `_apply_read_filters(...)`:

- `user_id`
- `date_from`
- `date_to`
- `transaction_type`
- `category_key`

## Transaction Schemas

File: `src/schemas.py`.

Analytics response schemas:

- `TransactionAnalyticsOverview`
- `TransactionAnalyticsByCategory`
- `TransactionAnalyticsTimeseries`

Canonical transaction types:

- `income`
- `expense`

Legacy values are normalized for compatibility where supported.

## Technical Notes

- `Base.metadata.create_all(bind=engine)` is still used at startup.
- No Alembic migration is configured yet.
- CORS is currently permissive and should be restricted before production hardening.
- Local direct run port is `8001`.
- Docker exposes `5001`.
