# src/schemas.py
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
import uuid
import enum

class TransactionType(str, enum.Enum):
    expense = "expense"
    income  = "income"

class TransactionBase(BaseModel):
    type: TransactionType
    amount: float
    occurred: Optional[datetime] = None
    category: Optional[str] = None
    note: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionRead(TransactionBase):
    id: uuid.UUID
    owner_id: uuid.UUID

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str

class UserCreate(BaseModel):
    username: str = Field(..., min_length=2, description="Username không được để trống")
    password: str = Field(..., min_length=4, description="Password không được để trống")
    fullname: Optional[str] = Field(None, description="Họ tên đầy đủ, có thể để trống")
    
class UserUpdate(BaseModel):
    password: str = Field(None, min_length=4, description="Mật khẩu mới, tối thiểu 4 kí tự"
)
    fullname: Optional[str] = None
    
class UserRead(BaseModel):
    id: uuid.UUID
    username: str

    class Config:
        orm_mode = True