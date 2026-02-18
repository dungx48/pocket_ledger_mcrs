# src/controller/category_controller.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.schemas import CategoryRead
from src.repository.category_repository import CategoryRepository
from src.service.category_service import CategoryService
from src.utils.database import get_db

router = APIRouter(tags=["categories"])


def get_category_service(db: Session = Depends(get_db)):
    repo = CategoryRepository(db)
    return CategoryService(repo)


@router.get("/", response_model=list[CategoryRead])
def list_categories(
    svc: CategoryService = Depends(get_category_service),
):
    return svc.list_categories()
