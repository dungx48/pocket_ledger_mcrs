# src/controller/auth_controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.utils.database import get_db
from src.utils.security import AuthService

router = APIRouter(tags=["auth"])

@router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    svc = AuthService(db)
    user = svc.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect credentials")
    access_token = svc.create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
