# src/models/transaction.py
from sqlalchemy import Column, Numeric, DateTime, Text, Enum, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid, enum
from src.utils.database import Base

class TransactionType(enum.Enum):
    expense = "expense"
    income  = "income"

class Transaction(Base):
    __tablename__ = "transactions"

    id        = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id  = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    type      = Column(Enum(TransactionType), nullable=False)
    amount    = Column(Numeric(12,2), nullable=False)
    occurred  = Column(DateTime(timezone=True), server_default=func.now())
    category  = Column(Text, nullable=True)
    note      = Column(Text, nullable=True)

    # Thiết lập quan hệ với User
    owner = relationship("User", back_populates="transactions")