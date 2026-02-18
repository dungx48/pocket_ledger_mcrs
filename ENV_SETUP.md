# ENV_SETUP

## 1. Yêu cầu môi trường

- Python `3.9+` (khuyến nghị cùng bản trong Dockerfile: `3.9`)
- PostgreSQL `13+` (hoặc tương đương)
- `pip` để cài dependencies
- (Tùy chọn) Docker + Docker Compose

## 2. Biến môi trường

Tạo file `.env` ở root project:

```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=pocket_ledger
JWT_SECRET=change_me_to_a_long_random_secret
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Các biến này được load bởi `src/utils/config.py`.

## 3. Cấu hình PostgreSQL

1. Tạo database:
```sql
CREATE DATABASE pocket_ledger;
```
2. Kết nối vào DB và bật extension UUID:
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

Lý do: bảng `fact_transactions` dùng default `uuid_generate_v4()`.

## 4. Chạy local

1. Tạo virtualenv:
```bash
python -m venv .venv
source .venv/bin/activate
```
2. Cài dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
3. Chạy app:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload
```
4. Kiểm tra:
- Health: `http://localhost:8001/health`
- Swagger: `http://localhost:8001/docs`

## 5. Chạy bằng Docker

```bash
docker compose up --build
```

Sau khi chạy:

- API: `http://localhost:5001`
- Swagger: `http://localhost:5001/docs`

## 6. Luồng auth cơ bản để test API

1. Gọi `POST /auth/token` với form-data:
- `username`
- `password`
2. Nhận `access_token`.
3. Gửi header:
```http
Authorization: Bearer <access_token>
```

## 7. Troubleshooting nhanh

- `401 Unauthorized`:
- kiểm tra token có hết hạn không
- kiểm tra `JWT_SECRET` có thay đổi không

- Lỗi `function uuid_generate_v4() does not exist`:
- chưa bật extension `uuid-ossp`

- Kết nối DB fail:
- kiểm tra `DB_HOST/DB_PORT/DB_USER/DB_PASSWORD/DB_NAME` trong `.env`

- Port không đúng:
- local mặc định `8001`
- docker mặc định `5001`
