# src/models/category.py

from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship
import enum

from src.utils.database import Base

class CategoryType(enum.Enum):
    expense = "expense"
    income = "income"
    
class Category(Base):
    __tablename__ = "categories"
    id = Column(String(6), primary_key=True)
    description = Column(String(255), nullable=False)
    type = Column(Enum(CategoryType), nullable=False)
    
    transactions = relationship("Transaction", back_populates="category")

