from sqlalchemy.orm import Session
from sqlalchemy import case, func
from uuid import UUID
from typing import Optional
from datetime import date, timedelta
from src.model.transaction import Transaction
from src.schemas import (
    EXPENSE_TRANSACTION_VALUES,
    INCOME_TRANSACTION_VALUES,
    TransactionCreate,
    TransactionUpdate,
)

class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(
        self,
        skip: int = 0,
        limit: int = 100,
        user_id: Optional[UUID] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
    ):
        q = self.db.query(Transaction)
        q = self._apply_read_filters(q, user_id=user_id, date_from=date_from, date_to=date_to)
        return q.order_by(Transaction.date.desc(), Transaction.created_at.desc()).offset(skip).limit(limit).all()

    def monthly_summary(
        self,
        user_id: Optional[UUID] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
    ):
        month = func.to_char(Transaction.date, "YYYY-MM").label("month")
        q = self.db.query(
            month,
            self._expense_sum().label("expense"),
            self._income_sum().label("income"),
            func.count(Transaction.id).label("transaction_count"),
        )
        q = self._apply_read_filters(q, user_id=user_id, date_from=date_from, date_to=date_to)
        rows = q.group_by(month).order_by(month.desc()).all()
        return [
            {
                "month": row.month,
                "expense": row.expense or 0,
                "income": row.income or 0,
                "transaction_count": row.transaction_count or 0,
            }
            for row in rows
        ]

    def weekly_summary(
        self,
        date_from: date,
        date_to: date,
        user_id: Optional[UUID] = None,
    ):
        q = self.db.query(
            Transaction.date.label("date"),
            self._expense_sum().label("expense"),
            self._income_sum().label("income"),
            func.count(Transaction.id).label("transaction_count"),
        )
        q = self._apply_read_filters(q, user_id=user_id, date_from=date_from, date_to=date_to)
        daily_rows = q.group_by(Transaction.date).order_by(Transaction.date.asc()).all()

        bucket_by_start = {}
        current = date_from
        while current <= date_to:
            bucket_by_start[current] = {
                "week_start": current,
                "week_end": min(current + timedelta(days=6), date_to),
                "expense": 0,
                "income": 0,
                "transaction_count": 0,
            }
            current += timedelta(days=7)

        for row in daily_rows:
            days_from_start = (row.date - date_from).days
            bucket_start = date_from + timedelta(days=(days_from_start // 7) * 7)
            bucket = bucket_by_start[bucket_start]
            bucket["expense"] += row.expense or 0
            bucket["income"] += row.income or 0
            bucket["transaction_count"] += row.transaction_count or 0

        return list(bucket_by_start.values())

    def _apply_read_filters(
        self,
        q,
        user_id: Optional[UUID] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
    ):
        if user_id is not None:
            q = q.filter(Transaction.user_id == user_id)
        if date_from is not None:
            q = q.filter(Transaction.date >= date_from)
        if date_to is not None:
            q = q.filter(Transaction.date <= date_to)
        return q

    def _expense_sum(self):
        return func.coalesce(
            func.sum(
                case(
                    (self._normalized_transaction_type().in_(EXPENSE_TRANSACTION_VALUES), Transaction.amount),
                    else_=0,
                )
            ),
            0,
        )

    def _income_sum(self):
        return func.coalesce(
            func.sum(
                case(
                    (self._normalized_transaction_type().in_(INCOME_TRANSACTION_VALUES), Transaction.amount),
                    else_=0,
                )
            ),
            0,
        )

    def _normalized_transaction_type(self):
        return func.lower(func.trim(Transaction.transaction_type))

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
