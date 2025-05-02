# src/models/transaction.py

from sqlalchemy import Column, Numeric, Date, DateTime, Text, String, CheckConstraint, ForeignKey, func, text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.utils.database import Base
from .category import Category


class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = (
        Index("idx_tx_user_date", "user_id", "date"),
        Index("idx_tx_category", "category_id"),
        CheckConstraint("amount > 0", name="transactions_amount_check"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(String(6), ForeignKey("categories.id", ondelete="SET NULL"), nullable=False, index=True)
    amount = Column(Numeric(14, 2), nullable=False)
    date = Column(Date, nullable=False)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    owner = relationship("User", back_populates="transactions")
    category = relationship(
        "Category",
        back_populates="transactions",
        foreign_keys=[category_id]
    )