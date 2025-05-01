from sqlalchemy.orm import Session
import uuid
from typing import Optional

from src.model.user import User
from src.schemas import UserCreate


class UserRepository:
    """
    Repository for User model: thực hiện các thao tác CRUD liên quan tới User.
    """
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> Optional[User]:
        """
        Trả về đối tượng User có username tương ứng, hoặc None nếu không tìm thấy.
        """
        return self.db.query(User).filter(User.username == username).first()

    def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """
        Trả về User theo khoá chính ID, hoặc None nếu không tồn tại.
        """
        return self.db.query(User).get(user_id)

    def create(self, user_in: UserCreate, hashed_password: str) -> User:
        """
        Tạo mới User:
        - `user_in` chứa thông tin (username)
        - `hashed_password` đã hash sẵn
        """
        db_user = User(
            id=uuid.uuid4(),
            username=user_in.username,
            hashed_password=hashed_password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete(self, user_id: uuid.UUID) -> bool:
        """
        Xoá User theo ID, trả về True nếu xoá thành công, False nếu không tìm thấy.
        """
        user = self.get_by_id(user_id)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True
