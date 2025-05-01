# src/controller/user_controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.utils.database import get_db
from src.utils.security import AuthService, get_current_user
from src.repository.user_repository import UserRepository
from src.schemas import UserCreate, UserRead, UserUpdate
from src.model.user import User as UserModel

router = APIRouter(tags=["users"])

# Helper to enforce admin
def ensure_admin(user: UserModel):
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền")

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    ensure_admin(current_user)
    repo = UserRepository(db)
    if repo.get_by_username(user_in.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username đã tồn tại")
    auth = AuthService(db)
    hashed_pwd = auth.hash_password(user_in.password)
    user = repo.create(user_in, hashed_pwd)
    return user

@router.get("/", response_model=List[UserRead])
def list_users(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    ensure_admin(current_user)
    return UserRepository(db).get_all()

@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    ensure_admin(current_user)
    user = UserRepository(db).get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User không tồn tại")
    return user

@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: str,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    ensure_admin(current_user)
    repo = UserRepository(db)
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User không tồn tại")
    auth = AuthService(db)
    hashed = auth.hash_password(user_in.password) if user_in.password else None
    user = repo.update(user, user_in, hashed)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    ensure_admin(current_user)
    success = UserRepository(db).delete(user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User không tồn tại")