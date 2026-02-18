## Pocket Ledger Backend

Backend API cho ứng dụng quản lý thu chi cá nhân, xây dựng bằng FastAPI + SQLAlchemy + PostgreSQL.

## Tài liệu chính

- Kiến trúc hệ thống: `ARCHITECTURE.md`
- Cấu trúc thư mục: `PROJECT_STRUCTURE.md`
- Cấu hình môi trường và cách chạy: `ENV_SETUP.md`

## Tóm tắt nhanh

- Framework: FastAPI
- ORM: SQLAlchemy
- DB: PostgreSQL
- Auth: JWT Bearer Token (`/auth/token`)
- Router hiện có:
- `GET /health`
- `POST /auth/token`
- `/users` (quản lý user, chỉ admin)
- `/transactions` (CRUD giao dịch theo quyền user/admin)
- `/categories` (danh mục category)

## Chạy nhanh

1. Cài dependencies:
```bash
pip install -r requirements.txt
```
2. Tạo `.env` (xem mẫu trong `ENV_SETUP.md`).
3. Chạy app local:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload
```
4. Mở docs:
- Swagger UI: `http://localhost:8001/docs`

## Lưu ý quan trọng

- Local mặc định dùng port `8001` (`src/main.py`), còn Docker expose `5001`.
- Bảng `fact_transactions.id` dùng `uuid_generate_v4()`, cần bật extension PostgreSQL:
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```
