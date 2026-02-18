# src/models/category.py

from sqlalchemy import Column, String
from src.utils.database import Base

    
class Category(Base):
    __tablename__ = "dim_categories"
    id = Column(String(6), primary_key=True)
    description = Column(String(255), nullable=False)
    key =  Column(String(10), nullable=False)
    value = Column(String(50), nullable=False)
    is_active = Column(String(5), nullable=False)
    table_name = Column(String(50), nullable=False)
    field_name = Column(String(50), nullable=False)