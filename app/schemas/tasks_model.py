

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class TaskBase(BaseModel):
    title: str = Field(min_length=1)
    description: Optional[str] = None
    completed: bool = False


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = None
    completed: Optional[bool] = None


class Task(TaskBase):
    id: UUID
