# src/repository/transaction_repository.py
from sqlalchemy.orm import Session
from src.model.transaction import Transaction
from src.schemas import TransactionCreate

class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self, skip: int = 0, limit: int = 100):
        return self.db.query(Transaction).offset(skip).limit(limit).all()

    def get(self, txn_id):
        return self.db.query(Transaction).get(txn_id)

    def create(self, data: TransactionCreate, owner_id):
        db_txn = Transaction(**data.dict(), owner_id=owner_id)
        self.db.add(db_txn)
        self.db.commit()
        self.db.refresh(db_txn)
        return db_txn

    def delete(self, txn_id):
        obj = self.get(txn_id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
        return obj
