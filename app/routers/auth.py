from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import AuthCreate
from app.models import User
from app.auth import verify_password, create_access_token
router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/")
def login(login: AuthCreate, db: Session = Depends(get_db)):
    """Retorna el token de acceso"""
    db_email = db.query(User).filter(User.email == login.email).first()
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
