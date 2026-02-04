
from fastapi import FastAPI
from app.routes.tasks import router as tasks_router


app = FastAPI(
    title="Task Management API",
    description="API for managing tasks with create, read, update, and delete operations.",
    version="1.0.0",
)
app.include_router(tasks_router)
           
           

