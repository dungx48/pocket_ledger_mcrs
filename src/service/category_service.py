# src/service/category_service.py
from src.repository.category_repository import CategoryRepository

class CategoryService:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    def list_categories(self):
        return self.repo.get_all()
