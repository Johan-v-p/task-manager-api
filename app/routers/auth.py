from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.auth import verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/login")
def login(login: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm), db: Session = Depends(get_db)):
    """Retorna el token de acceso"""
    db_email = db.query(User).filter(User.email == login.username).first()
    if db_email is None:
        raise HTTPException(status_code=401, detail='Error el usuario no existe')
    
    if not verify_password(login.password, db_email.password):
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )
    
    access_token = create_access_token({"sub": db_email.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
