# src/controller/transaction_controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.schemas import TransactionRead, TransactionCreate
from src.repository.transaction_repository import TransactionRepository
from src.service.transaction_service import TransactionService
from src.utils.database import get_db
from src.utils.security import get_current_user

router = APIRouter(prefix="/transactions", tags=["transactions"])

def get_txn_service(db: Session = Depends(get_db)):
    repo = TransactionRepository(db)
    return TransactionService(repo)

@router.get("/", response_model=list[TransactionRead])
def list_txns(
    skip: int = 0,
    limit: int = 100,
    svc: TransactionService = Depends(get_txn_service),
    current_user=Depends(get_current_user)
):
    return svc.list_transactions(skip, limit)

@router.post("/", response_model=TransactionRead)
def create_txn(
    payload: TransactionCreate,
    svc: TransactionService = Depends(get_txn_service),
    current_user=Depends(get_current_user)
):
    return svc.create_transaction(payload, owner_id=current_user.id)
