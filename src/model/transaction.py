# src/models/transaction.py

from sqlalchemy import Column, Numeric, Date, DateTime, Text, String, CheckConstraint, func, text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.utils.database import Base
from .category import Category


class Transaction(Base):
    __tablename__ = "fact_transactions"
    __table_args__ = (
        Index("idx_tx_user_date", "user_id", "date"),
        Index("idx_tx_category", "category_key"),
        CheckConstraint("amount > 0", name="transactions_amount_check"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    user_id = Column(UUID(as_uuid=True), nullable=False)
    category_key = Column(String(6), nullable=False, index=True)
    amount = Column(Numeric(14, 2), nullable=False)
    date = Column(Date, nullable=False)
    note = Column(Text, nullable=True)
    transaction_type = Column(String(10), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())