# src/schemas.py
from __future__ import annotations

from datetime import date, datetime
from pydantic import BaseModel, Field
from typing import Optional, Annotated
import uuid
import enum


class CategoryType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"


class CategoryBase(BaseModel):
    id: Annotated[str, Field(..., min_length=2, max_length=6, description="Mã category, 2-6 ký tự")]
    description: Annotated[str, Field(..., description="Mô tả chi tiết của category")]
    type: Annotated[CategoryType, Field(..., description="Kiểu category: income hoặc expense")]


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    model_config = {"from_attributes": True}


class TransactionBase(BaseModel):
    amount: Annotated[float, Field(..., gt=0, description="Số tiền giao dịch, phải lớn hơn 0")]
    date: Annotated[date, Field(..., description="Ngày giao dịch")]
    category_id: Annotated[str, Field(..., min_length=2, max_length=6, description="Mã category liên kết")]
    note: Annotated[Optional[str], Field(None, description="Ghi chú")]

    model_config = {"from_attributes": True}


class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    date:   Optional[date]  = None
    category_id: Optional[str] = Field(None, min_length=2, max_length=6)
    note:   Optional[str]  = None

    model_config = {"from_attributes": True}

class TransactionRead(TransactionBase):
    id: Annotated[uuid.UUID, Field(...)]
    user_id: Annotated[uuid.UUID, Field(...)]
    created_at: Annotated[datetime, Field(...)]

    model_config = {"from_attributes": True}


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