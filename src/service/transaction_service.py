# src/service/transaction_service.py
from src.repository.transaction_repository import TransactionRepository

class TransactionService:
    def __init__(self, repo: TransactionRepository):
        self.repo = repo

    def list_transactions(self, skip: int, limit: int):
        return self.repo.list(skip, limit)

    def create_transaction(self, data, owner_id):
        # ví dụ: kiểm tra business rule, validate thêm…
        return self.repo.create(data, owner_id)
