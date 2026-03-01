from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from app.schemas.task import TaskRead


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ProjectCreate(ProjectBase):
    model_config = ConfigDict(from_attributes=True)


class ProjectRead(ProjectBase):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    tasks: List[TaskRead] = []

    model_config = ConfigDict(from_attributes=True)

class ProjectUpdate(ProjectBase):
    name: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)