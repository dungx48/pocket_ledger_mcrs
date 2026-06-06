# src/service/transaction_service.py
from uuid import UUID
from datetime import date
from typing import Optional
from src.repository.transaction_repository import TransactionRepository
from src.schemas import TransactionCreate, normalize_transaction_type
from src.schemas import UserRead

class TransactionService:
    def __init__(self, repo: TransactionRepository):
        self.repo = repo

    def list_transactions(self, skip: int, limit: int, current_user: UserRead, date_from: Optional[date] = None, date_to: Optional[date] = None):
        if current_user.is_admin:
            return self.repo.list(skip, limit, date_from=date_from, date_to=date_to)
        return self.repo.list(skip, limit, user_id=current_user.id, date_from=date_from, date_to=date_to)

    def monthly_summary(self, current_user: UserRead, date_from: Optional[date] = None, date_to: Optional[date] = None):
        if current_user.is_admin:
            return self.repo.monthly_summary(date_from=date_from, date_to=date_to)
        return self.repo.monthly_summary(user_id=current_user.id, date_from=date_from, date_to=date_to)

    def weekly_summary(self, current_user: UserRead, date_from: date, date_to: date):
        if current_user.is_admin:
            return self.repo.weekly_summary(date_from=date_from, date_to=date_to)
        return self.repo.weekly_summary(date_from=date_from, date_to=date_to, user_id=current_user.id)

    def analytics_overview(
        self,
        current_user: UserRead,
        date_from: date,
        date_to: date,
        transaction_type: Optional[str] = None,
        category_key: Optional[str] = None,
    ):
        normalized_type = normalize_transaction_type(transaction_type) if transaction_type else None
        if current_user.is_admin:
            return self.repo.analytics_overview(
                date_from=date_from,
                date_to=date_to,
                transaction_type=normalized_type,
                category_key=category_key,
            )
        return self.repo.analytics_overview(
            date_from=date_from,
            date_to=date_to,
            user_id=current_user.id,
            transaction_type=normalized_type,
            category_key=category_key,
        )

    def analytics_by_category(
        self,
        current_user: UserRead,
        date_from: date,
        date_to: date,
        transaction_type: Optional[str] = None,
        category_key: Optional[str] = None,
    ):
        normalized_type = normalize_transaction_type(transaction_type) if transaction_type else None
        if current_user.is_admin:
            return self.repo.analytics_by_category(
                date_from=date_from,
                date_to=date_to,
                transaction_type=normalized_type,
                category_key=category_key,
            )
        return self.repo.analytics_by_category(
            date_from=date_from,
            date_to=date_to,
            user_id=current_user.id,
            transaction_type=normalized_type,
            category_key=category_key,
        )

    def analytics_timeseries(
        self,
        current_user: UserRead,
        date_from: date,
        date_to: date,
        group_by: str = "day",
        transaction_type: Optional[str] = None,
        category_key: Optional[str] = None,
    ):
        normalized_type = normalize_transaction_type(transaction_type) if transaction_type else None
        if current_user.is_admin:
            return self.repo.analytics_timeseries(
                date_from=date_from,
                date_to=date_to,
                group_by=group_by,
                transaction_type=normalized_type,
                category_key=category_key,
            )
        return self.repo.analytics_timeseries(
            date_from=date_from,
            date_to=date_to,
            user_id=current_user.id,
            group_by=group_by,
            transaction_type=normalized_type,
            category_key=category_key,
        )

    def create_transaction(self, data: TransactionCreate, current_user: UserRead):
        return self.repo.create(data, user_id=current_user.id)

    def patch_transaction(self, txn_id: UUID, data: TransactionCreate, current_user: UserRead):
        # lấy transaction, kiểm tra quyền
        txn = self.repo.get(txn_id)
        if not txn or (not current_user.is_admin and txn.user_id != current_user.id):
            return None
        return self.repo.update(txn_id, data)

    def delete_transaction(self, txn_id: UUID, current_user: UserRead):
        txn = self.repo.get(txn_id)
        if not txn or (not current_user.is_admin and txn.user_id != current_user.id):
            return None
        return self.repo.delete(txn_id)
