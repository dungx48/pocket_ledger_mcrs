import threading
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from .config import settings

class PostgreDatabase:
    """
    Singleton Database: khởi engine + SessionLocal + Base 1 lần duy nhất
    Context-manager session() sẽ commit/rollback + đóng session tự động.
    """
    _instance = None
    _lock = threading.Lock()    # đảm bảo thread-safe nếu đa luồng

    Base = declarative_base()   # mọi model sẽ kế thừa từ đây

    def __new__(cls):
        # Singleton: nếu chưa có instance thì tạo
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init_engine()
        return cls._instance

    def _init_engine(self):
        url = (
            f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}"
            f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
        )
        self.engine = create_engine(
            url,
            pool_pre_ping=True,
        )
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
        )

# Tạo sẵn instance để import
db = PostgreDatabase()

# Xuất ra module-level cho các phần khác dùng
Base   = db.Base
engine = db.engine

# Định nghĩa generator get_db() cho FastAPI Dependency

def get_db():
    """
    FastAPI dependency: yield một Session và tự close sau request.
    """
    db_session: Session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
