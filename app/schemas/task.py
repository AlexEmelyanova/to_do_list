from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    priority: Optional[int] = None
    note: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class TaskCreate(TaskBase):
    project_id: int

    model_config = ConfigDict(from_attributes=True)

class TaskRead(TaskBase):
    id: int
    is_completed: bool
    project_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TaskUpdate(TaskBase):
    title: Optional[str] = None
    is_completed: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)