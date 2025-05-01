# src/models/user.py
import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.utils.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    username = Column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )
    hashed_password = Column(
        String,
        nullable=False,
    )
    full_name = Column(
        String(50)
    )
    is_admin = Column(
        Boolean, 
        default=False
    )


    # Quan hệ 1 user có nhiều transactions
    transactions = relationship(
        "Transaction", 
        back_populates="owner",
        cascade="all, delete-orphan"
    )
