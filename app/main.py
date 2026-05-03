from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers.users import router as users_router
from app.routers.tasks import router as tasks_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return {"mensaje": "Bienvenido al Task Manager"}

@app.get("/status")
def get_status():
    return {"status": "ok"}

app.include_router(users_router)
app.include_router(tasks_router)