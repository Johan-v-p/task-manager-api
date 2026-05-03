from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.get("/", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    """Retorna todas las tareas"""
    tasks = db.query(Task).filter(Task.is_active == True).all()
    return tasks

@router.post("/", response_model=TaskResponse)
def crear_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Crea tareas nueva"""
    db_task = db.query(Task).filter(Task.user_id == task.user_id).filter(Task.title == task.title).first()
    if db_task is not None:
        raise HTTPException(status_code=409, detail="Error la tarea ya existe")
    new_task = Task(**task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/{id}", response_model=TaskResponse)
def get_task(id: int, db: Session = Depends(get_db)):
    """retorna una tarea por su id"""
    task = db.query(Task).filter(Task.id == id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Error Tarea no encontrada")
    return task

@router.patch("/{id}", response_model=TaskResponse)
def atualizar_task(id: int, task:TaskUpdate, db: Session = Depends(get_db)):
    """Atualiza una tarea por id"""
    db_task = db.query(Task).filter(Task.id == id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Error Tarea no encontrada")
    data = task.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)

    return db_task

@router.delete("/{id}")
def delete_task(id: int, db: Session = Depends(get_db)):
    """elimina una tarea por su id"""
    db_task = db.query(Task).filter(Task.id == id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Error tarea no encontrada")
    
    db_task.is_active = False
    db.commit()
    return {
        "mensaje": "Tarea eliminada con exito"
    }
        
    