# src/schemas.py
from __future__ import annotations

from datetime import date, datetime
from pydantic import BaseModel, Field
from typing import Optional, Annotated
import uuid


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
    date: Annotated[date, Field(..., description="Ngày giao dịch")]
    note: Annotated[Optional[str], Field(None, description="Ghi chú")]
    transaction_type: Annotated[str, Field(..., max_length=10, description="Loại giao dịch: thu hoặc chi")]

    model_config = {"from_attributes": True}


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    category_key: Optional[str] = None
    amount: Optional[float] = Field(None, gt=0)
    date: Optional[date] = None
    note: Optional[str] = None

    model_config = {"from_attributes": True}


class TransactionRead(TransactionBase):
    id: Annotated[uuid.UUID, Field(...)]
    user_id: Annotated[uuid.UUID, Field(...)]
    created_at: Annotated[datetime, Field(...)]

    model_config = {"from_attributes": True}


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