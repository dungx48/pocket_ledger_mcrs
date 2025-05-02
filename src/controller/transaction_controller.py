# src/controller/transaction_controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from sqlalchemy.orm import Session

from src.schemas import TransactionRead, TransactionCreate, TransactionUpdate
from src.repository.transaction_repository import TransactionRepository
from src.service.transaction_service import TransactionService
from src.utils.database import get_db
from src.utils.security import get_current_user

router = APIRouter(tags=["transactions"])


def get_txn_service(db: Session = Depends(get_db)):
    repo = TransactionRepository(db)
    return TransactionService(repo)

@router.get("/", response_model=list[TransactionRead])
def list_txns(
    skip: int = 0,
    limit: int = 100,
    svc: TransactionService = Depends(get_txn_service),
    current_user=Depends(get_current_user),
):
    return svc.list_transactions(skip, limit, current_user)


@router.post("/", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
def create_txn(
    payload: TransactionCreate,
    svc: TransactionService = Depends(get_txn_service),
    current_user=Depends(get_current_user),
):
    return svc.create_transaction(payload, current_user)


@router.patch("/{txn_id}", response_model=TransactionRead)
def update_txn(
    txn_id: UUID,
    payload: TransactionUpdate,
    svc: TransactionService = Depends(get_txn_service),
    current_user=Depends(get_current_user),
):
    updated = svc.patch_transaction(txn_id, payload, current_user)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction không tồn tại hoặc không có quyền")
    return updated


@router.delete("/{txn_id}", response_model=TransactionRead)
def delete_txn(
    txn_id: UUID,
    svc: TransactionService = Depends(get_txn_service),
    current_user=Depends(get_current_user),
):
    deleted = svc.delete_transaction(txn_id, current_user)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction không tồn tại hoặc không có quyền")
    return deleted
