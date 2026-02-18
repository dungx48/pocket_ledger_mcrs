# ARCHITECTURE

## 1. Tổng quan

Project theo mô hình phân lớp:

- `controller`: nhận HTTP request/response.
- `service`: xử lý nghiệp vụ.
- `repository`: truy cập dữ liệu DB qua SQLAlchemy Session.
- `model`: định nghĩa bảng DB.
- `schemas`: contract request/response bằng Pydantic.
- `utils`: cấu hình, database singleton, security (JWT + password hash).
- `middleware`: logging request.

Entry point là `src/main.py`.

## 2. Thành phần runtime

- FastAPI app: khai báo router, middleware, CORS.
- SQLAlchemy engine/session: khởi tạo trong `src/utils/database.py`.
- PostgreSQL: lưu dữ liệu users, transactions, categories.
- JWT auth:
- login qua `POST /auth/token`
- các API cần xác thực dùng `Depends(get_current_user)`

## 3. Luồng request

Luồng chuẩn:

1. HTTP request đi vào `FastAPI`.
2. `SafeLoggingMiddleware` ghi log method/path/status/duration.
3. Router ở `controller` nhận request.
4. Router gọi `service` (hoặc repository trực tiếp ở một số controller).
5. `service` thực thi nghiệp vụ, phân quyền.
6. `repository` thao tác DB qua `Session`.
7. Kết quả trả về, FastAPI serialize theo `schemas`.

## 4. Auth & phân quyền

### 4.1 Xác thực

- `AuthService.authenticate(username, password)` kiểm tra user + bcrypt hash.
- Token JWT tạo bằng `HS256`, secret lấy từ `JWT_SECRET`.
- Payload chứa `sub=username`, `exp`.

### 4.2 Kiểm tra user hiện tại

- `get_current_user`:
- đọc bearer token từ `Authorization`
- decode JWT
- lấy user từ DB theo username
- fail thì trả `401 Unauthorized`

### 4.3 Phân quyền

- `users` API yêu cầu admin (`ensure_admin` trong `user_controller`).
- `transactions`:
- admin xem/sửa/xóa tất cả.
- user thường chỉ thao tác transaction của chính mình.
- `categories`: hiện tại cho phép đọc danh sách.

## 5. Dữ liệu & schema

### 5.1 Bảng chính

- `fact_users` (`src/model/user.py`)
- `id` UUID
- `username` unique
- `hashed_password`
- `full_name`
- `is_admin`

- `fact_transactions` (`src/model/transaction.py`)
- `id` UUID, default `uuid_generate_v4()`
- `user_id` UUID
- `category_key`
- `amount` numeric(14,2), check `amount > 0`
- `date`, `note`, `transaction_type`, `created_at`
- index: `(user_id, date)`, `(category_key)`

- `dim_categories` (`src/model/category.py`)
- `id`, `description`, `key`, `value`, `is_active`, `table_name`, `field_name`

### 5.2 Pydantic schemas

Nằm trong `src/schemas.py`:

- Category: `CategoryCreate/Read/Update`
- Transaction: `TransactionCreate/Read/Update`
- User: `UserCreate/Read/Update`

## 6. Dependency wiring

- DB Session qua `Depends(get_db)` (mỗi request 1 session, tự close).
- Transaction service qua `get_txn_service`.
- Category service qua `get_category_service`.
- Current user qua `Depends(get_current_user)`.

## 7. Middleware & cross-cutting concerns

- `SafeLoggingMiddleware`: log request timing.
- CORS: currently `allow_origins=["*"]`, `allow_methods=["*"]`, `allow_headers=["*"]`.

## 8. Điểm cần lưu ý kỹ thuật

- `Base.metadata.create_all(bind=engine)` tự tạo bảng khi app start.
- Không có migration tool (Alembic) trong repo hiện tại.
- Local run port là `8001`, Docker run port là `5001`.
- DB cần extension `uuid-ossp` để `uuid_generate_v4()` hoạt động.
