# src/schemas.py
from __future__ import annotations

from datetime import date as date_type, datetime
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Annotated, Union
import uuid


INCOME_TRANSACTION_TYPE = "1"
EXPENSE_TRANSACTION_TYPE = "2"
INCOME_TRANSACTION_VALUES = {"1"}
EXPENSE_TRANSACTION_VALUES = {"2"}


def normalize_transaction_type(value: str | int | None) -> str:
    normalized = str(value or "").strip().lower()
    if normalized in INCOME_TRANSACTION_VALUES:
        return INCOME_TRANSACTION_TYPE
    if normalized in EXPENSE_TRANSACTION_VALUES:
        return EXPENSE_TRANSACTION_TYPE
    raise ValueError("transaction_type must be 1 or 2")


# =========================
# Category
# =========================
class CategoryBase(BaseModel):
    description: Annotated[str, Field(..., max_length=255, description="Mô tả chi tiết của category")]
    key: Annotated[str, Field(..., min_length=1, max_length=10, description="Key category (tối đa 10 ký tự)")]
    value: Annotated[str, Field(..., min_length=1, max_length=50, description="Value category (tối đa 50 ký tự)")]
    is_active: Annotated[str, Field(..., max_length=5, description="Trạng thái hoạt động của category")]
    table_name: Annotated[str, Field(..., max_length=50)]
    field_name: Annotated[str, Field(..., max_length=50)]
    
class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    model_config = {"from_attributes": True}


class CategoryRead(CategoryBase):
    id: Annotated[uuid.UUID, Field(..., description="UUID của category")]

    model_config = {"from_attributes": True}


# =========================
# Transaction
# =========================
class TransactionBase(BaseModel):
    category_key: Annotated[str, Field(..., description="key category liên kết")]
    amount: Annotated[float, Field(..., gt=0, description="Số tiền giao dịch, phải lớn hơn 0")]
    date: Annotated[date_type, Field(..., description="Ngày giao dịch")]
    note: Annotated[Optional[str], Field(None, description="Ghi chú")]
    transaction_type: Annotated[str, Field(..., max_length=10, description="Loại giao dịch: thu hoặc chi")]

    model_config = {"from_attributes": True}

    @field_validator("transaction_type", mode="before")
    @classmethod
    def validate_transaction_type(cls, value):
        return normalize_transaction_type(value)


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    category_key: Optional[str] = None
    amount: Optional[float] = Field(None, gt=0)
    date: Optional[date_type] = None
    note: Optional[str] = None
    transaction_type: Optional[str] = None

    model_config = {"from_attributes": True}

    @field_validator("transaction_type", mode="before")
    @classmethod
    def validate_transaction_type(cls, value):
        if value is None:
            return None
        return normalize_transaction_type(value)


class TransactionRead(TransactionBase):
    id: Annotated[uuid.UUID, Field(...)]
    user_id: Annotated[uuid.UUID, Field(...)]
    created_at: Annotated[datetime, Field(...)]

    model_config = {"from_attributes": True}


class TransactionMonthlySummary(BaseModel):
    month: Annotated[str, Field(..., description="Thang tong hop, dinh dang YYYY-MM")]
    expense: Annotated[float, Field(..., description="Tong tien chi trong thang")]
    income: Annotated[float, Field(..., description="Tong tien thu trong thang")]
    transaction_count: Annotated[int, Field(..., description="So giao dich trong thang")]


class TransactionWeeklySummary(BaseModel):
    week_start: Annotated[date_type, Field(..., description="Ngay bat dau tuan, inclusive")]
    week_end: Annotated[date_type, Field(..., description="Ngay ket thuc tuan, inclusive")]
    expense: Annotated[float, Field(..., description="Tong tien chi trong tuan")]
    income: Annotated[float, Field(..., description="Tong tien thu trong tuan")]
    transaction_count: Annotated[int, Field(..., description="So giao dich trong tuan")]


class TransactionAnalyticsOverview(BaseModel):
    date_from: Annotated[date_type, Field(..., description="Ngay bat dau khoang thong ke, inclusive")]
    date_to: Annotated[date_type, Field(..., description="Ngay ket thuc khoang thong ke, inclusive")]
    income: Annotated[float, Field(..., description="Tong tien thu trong khoang thoi gian")]
    expense: Annotated[float, Field(..., description="Tong tien chi trong khoang thoi gian")]
    balance: Annotated[float, Field(..., description="Thu nhap tru chi tieu")]
    transaction_count: Annotated[int, Field(..., description="So giao dich trong khoang thoi gian")]


class TransactionAnalyticsByCategory(BaseModel):
    category_key: Annotated[str, Field(..., description="Key danh muc giao dich")]
    amount: Annotated[float, Field(..., description="Tong tien cua danh muc")]
    transaction_count: Annotated[int, Field(..., description="So giao dich cua danh muc")]
    percentage: Annotated[float, Field(..., description="Ty le phan tram tren tong tien filter")]


class TransactionAnalyticsTimeseries(BaseModel):
    period: Annotated[str, Field(..., description="Ky thong ke theo group_by")]
    income: Annotated[float, Field(..., description="Tong tien thu trong ky")]
    expense: Annotated[float, Field(..., description="Tong tien chi trong ky")]
    balance: Annotated[float, Field(..., description="Thu nhap tru chi tieu trong ky")]
    transaction_count: Annotated[int, Field(..., description="So giao dich trong ky")]


# =========================
# User
# =========================
class UserBase(BaseModel):
    username: Annotated[str, Field(..., min_length=2)]


class UserCreate(BaseModel):
    username: Annotated[str, Field(..., min_length=2, description="Username không được để trống")]
    password: Annotated[str, Field(..., min_length=4, description="Password không được để trống")]
    fullname: Annotated[Optional[str], Field(None, description="Họ tên đầy đủ, có thể để trống")]

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    password: Annotated[Optional[str], Field(None, min_length=4, description="Mật khẩu mới, tối thiểu 4 kí tự")]
    fullname: Annotated[Optional[str], Field(None, description="Họ tên đầy đủ, có thể để trống")]

    model_config = {"from_attributes": True}


class UserRead(BaseModel):
    id: Annotated[uuid.UUID, Field(...)]
    username: Annotated[str, Field(...)]
    fullname: Annotated[Optional[str], Field(None)]
    is_admin: Annotated[bool, Field(..., description="Quyền admin (True nếu là admin)")]

    model_config = {"from_attributes": True}
