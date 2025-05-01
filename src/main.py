# src/main.py

import uvicorn
from fastapi import FastAPI
from src.utils.database import Base, engine, get_db
from src.controller.transaction_controller import router as txn_router
from src.controller.auth_controller import router as auth_router
from src.controller.user_controller import router as user_router

# 1. Tạo tất cả bảng nếu chưa có
Base.metadata.create_all(bind=engine)

# 2. Khởi FastAPI app
app = FastAPI(title="Pocket Ledger API")

# 3. Include các router
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(txn_router, prefix="/transactions", tags=["transactions"])
app.include_router(user_router, prefix="/users", tags=["users"])

# 4. Một route test để kiểm tra server đang chạy
@app.get("/health")
def health_check():
    return {"status": "ok"}

# 5. Chạy server khi chạy module này trực tiếp
if __name__ == "__main__":
    uvicorn.run(
        "src.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )
