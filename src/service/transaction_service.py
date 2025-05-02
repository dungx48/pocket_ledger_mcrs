# src/service/transaction_service.py
from uuid import UUID
from src.repository.transaction_repository import TransactionRepository
from src.schemas import TransactionCreate
from src.schemas import UserRead

class TransactionService:
    def __init__(self, repo: TransactionRepository):
        self.repo = repo

    def list_transactions(self, skip: int, limit: int, current_user: UserRead):
        if current_user.is_admin:
            return self.repo.list(skip, limit)
        return self.repo.list(skip, limit, user_id=current_user.id)

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
