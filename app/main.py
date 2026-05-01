from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"mensaje": "Bienvenido al Task Manager"}

@app.get("/status")
def get_status():
    return {"status": "ok"}