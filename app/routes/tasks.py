

from app.schemas.tasks_model import Task, TaskBase, TaskCreate, TaskUpdate
from fastapi import APIRouter, HTTPException
from uuid import UUID, uuid4


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},

)

DB_Tasks: list[Task] = []

@router.get("/", response_model=list[Task])
async def read_tasks():
    return DB_Tasks

@router.post("/", response_model=Task)
async def create_task(task: TaskCreate):
    for existing in DB_Tasks:
        if existing.title.strip().lower() == task.title.strip().lower():
            raise HTTPException(status_code=400, detail="Task already exists")
    new_task = Task(id=uuid4(), **task.model_dump())
    DB_Tasks.append(new_task)
    return new_task

@router.get("/{task_id}", response_model=Task)
async def read_task(task_id: UUID):
    for task in DB_Tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@router.patch("/{task_id}", response_model=Task)
async def update_task_partial(task_id: UUID, updated_task: TaskUpdate):
    task = next((t for t in DB_Tasks if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Only apply fields actually provided (and not null)
    updated_data = updated_task.model_dump(exclude_unset=True, exclude_none=True)
    if "title" in updated_data:
        new_title = updated_data["title"].strip().lower()
        for existing in DB_Tasks:
            if existing.id != task_id and existing.title.strip().lower() == new_title:
                raise HTTPException(status_code=400, detail="Task already exists")
    for key, value in updated_data.items():
        setattr(task, key, value)

    return task

@router.put("/{task_id}", response_model=Task)
async def update_task(task_id: UUID, updated_task: TaskBase):
    # Find the task
    task = next((t for t in DB_Tasks if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Full replace (all fields required)
    new_title = updated_task.title.strip().lower()
    for existing in DB_Tasks:
        if existing.id != task_id and existing.title.strip().lower() == new_title:
            raise HTTPException(status_code=400, detail="Task already exists")

    task.title = updated_task.title
    task.description = updated_task.description
    task.completed = updated_task.completed

    return task

        
@router.delete("/{task_id}")
async def delete_task(task_id: UUID):
    for task in DB_Tasks:
        if task.id == task_id:
            DB_Tasks.remove(task)
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")
