# src/schemas.py
from datetime import datetime
from pydantic import BaseModel
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

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
