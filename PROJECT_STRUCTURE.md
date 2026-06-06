# Project Structure

```text
pocket_ledger_mcrs/
  src/
    main.py
    schemas.py
    constant/
    controller/
      auth_controller.py
      category_controller.py
      transaction_controller.py
      user_controller.py
    middleware/
      logging.py
    model/
      category.py
      transaction.py
      user.py
    repository/
      category_repository.py
      transaction_repository.py
      user_repository.py
    service/
      category_service.py
      transaction_service.py
    utils/
      config.py
      database.py
      security.py
  Dockerfile
  docker-compose.yml
  requirements.txt
  README.md
  ARCHITECTURE.md
  PROJECT_STRUCTURE.md
  ENV_SETUP.md
```

## Key Files

- `src/main.py`: creates FastAPI app, adds middleware, includes routers and exposes health check.
- `src/schemas.py`: Pydantic request/response schemas, including transaction analytics schemas.
- `src/controller/transaction_controller.py`: transaction CRUD, summaries and analytics endpoints.
- `src/service/transaction_service.py`: transaction business logic and permission checks.
- `src/repository/transaction_repository.py`: transaction SQLAlchemy queries and aggregate logic.
- `src/model/transaction.py`: `fact_transactions` ORM model.
- `src/utils/security.py`: password hash, JWT creation/verification and current user dependency.
- `src/utils/database.py`: SQLAlchemy engine, session factory and `get_db`.

## Transaction Analytics Files

Analytics is implemented across:

- `src/controller/transaction_controller.py`
- `src/service/transaction_service.py`
- `src/repository/transaction_repository.py`
- `src/schemas.py`

Endpoint paths:

- `/transactions/analytics/overview`
- `/transactions/analytics/by-category`
- `/transactions/analytics/timeseries`

Supported analytics filters:

- `date_from`
- `date_to`
- `transaction_type`
- `category_key`
- `group_by` for timeseries

## Entry Points

Local:

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload
```

Docker:

- Container command is defined in `Dockerfile`.
- Compose exposes backend on port `5001`.

## Update Checklist

When changing transaction CRUD contract:

- Update `src/schemas.py`.
- Update `src/controller/transaction_controller.py`.
- Update `../docs/api-contract.md`.
- Update frontend `../pocket_ledger_mfe/lib/api.ts` if the frontend consumes the change.

When changing analytics contract:

- Update `src/schemas.py`.
- Update `src/controller/transaction_controller.py`.
- Update `src/service/transaction_service.py`.
- Update `src/repository/transaction_repository.py`.
- Update `../docs/api-contract.md`.
- Update frontend docs and `../pocket_ledger_mfe/lib/api.ts`.

When adding database schema changes:

- Prefer adding migration tooling first if the change is production-impacting.
- Keep `Base.metadata.create_all` limitations in mind.
