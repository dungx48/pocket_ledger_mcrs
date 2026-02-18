# PROJECT_STRUCTURE

## Cây thư mục chính

```text
pocket_ledger_mcrs/
├── src/
│   ├── main.py
│   ├── schemas.py
│   ├── constant/
│   ├── controller/
│   │   ├── auth_controller.py
│   │   ├── user_controller.py
│   │   ├── transaction_controller.py
│   │   └── category_controller.py
│   ├── middleware/
│   │   └── logging.py
│   ├── model/
│   │   ├── user.py
│   │   ├── transaction.py
│   │   └── category.py
│   ├── repository/
│   │   ├── user_repository.py
│   │   ├── transaction_repository.py
│   │   └── category_repository.py
│   ├── service/
│   │   ├── transaction_service.py
│   │   └── category_service.py
│   └── utils/
│       ├── config.py
│       ├── database.py
│       └── security.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── ARCHITECTURE.md
├── PROJECT_STRUCTURE.md
└── ENV_SETUP.md
```

## Vai trò từng nhóm file

- `src/main.py`: khởi tạo FastAPI app, add middleware, include routers, health check.
- `src/controller/`: định nghĩa endpoint HTTP.
- `src/service/`: nghiệp vụ (business logic), đặc biệt với transaction.
- `src/repository/`: thao tác DB bằng SQLAlchemy session.
- `src/model/`: định nghĩa bảng dữ liệu ORM.
- `src/schemas.py`: Pydantic schemas cho input/output API.
- `src/utils/config.py`: load biến môi trường bằng `pydantic-settings`.
- `src/utils/database.py`: singleton DB engine + session factory + `get_db`.
- `src/utils/security.py`: hash password, tạo/verify JWT, lấy user hiện tại.
- `src/middleware/logging.py`: middleware logging request.
- `Dockerfile`, `docker-compose.yml`: chạy app containerized.

## Entry points

- Dev local: `uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload`
- Docker: container expose `5001`, startup command trong `Dockerfile`
