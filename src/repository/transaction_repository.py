from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional
from src.model.transaction import Transaction
from src.schemas import TransactionCreate, TransactionUpdate

class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self, skip: int = 0, limit: int = 100, user_id: Optional[UUID] = None):
        q = self.db.query(Transaction)
        if user_id is not None:
            q = q.filter(Transaction.user_id == user_id)
        return q.offset(skip).limit(limit).all()

    def get(self, txn_id: UUID):
        return self.db.query(Transaction).get(txn_id)

    def create(self, data: TransactionCreate, user_id: UUID):
        db_txn = Transaction(**data.dict(), user_id=user_id)
        self.db.add(db_txn)
        self.db.commit()
        self.db.refresh(db_txn)
        return db_txn

    def update(self, txn_id: UUID, data: TransactionUpdate):
        db_txn = self.get(txn_id)
        update_data = data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_txn, field, value)
        self.db.commit()
        self.db.refresh(db_txn)
        return db_txn

    def delete(self, txn_id: UUID):
        obj = self.get(txn_id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
        return obj
