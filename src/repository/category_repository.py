# src/repository/category_repository.py
from sqlalchemy.orm import Session
from src.model.category import Category

class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Category]:
        return self.db.query(Category).order_by(Category.field_name.asc()).all()
