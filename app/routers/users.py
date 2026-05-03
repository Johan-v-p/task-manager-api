from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    """Retorna todos los usuarios"""
    
    users = db.query(User).filter(User.is_active == True).all()
    return users

@router.post("/", response_model=UserResponse)
def crear_users(user: UserCreate, db: Session = Depends(get_db)):
    """Crea usuario nuevo"""
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user is not None:
        raise HTTPException(status_code=409, detail='Error el usuario ya existe')
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    

@router.get("/{id}", response_model=UserResponse)
def get_user_id(id: int, db: Session = Depends(get_db)):
    """Retorna un usuario por su id"""
    user = db.query(User).filter(User.id == id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no Encontrado")
    return user

@router.patch("/{id}", response_model=UserResponse)
def atualizar_user(id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """Atualiza usuario por id"""
    db_user = db.query(User).filter(User.id == id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    data = user.model_dump(exclude_unset=True)
    for key, vuale in data.items():
        setattr(db_user, key, vuale)

    db.commit()
    db.refresh(db_user)

    return db_user

@router.delete("/{id}")
def borrar_user(id: int, db: Session = Depends(get_db)):
    """Elimina usuario por id"""
    db_user = db.query(User).filter(User.id == id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db_user.is_active = False
    db.commit()
    return {"mensaje" : "Usuario eliminado con exitosamente"}
    