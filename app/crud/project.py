from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, with_loader_criteria
from app.models import Project, Task
from app.schemas.project import ProjectCreate, ProjectUpdate

async def crud_create_project(db: AsyncSession, new_project: ProjectCreate, owner_id: str) -> Project:
    project = Project(**new_project.model_dump(), owner_id=owner_id)
    db.add(project)
    await db.commit()
    await db.refresh(project)
    result = await db.execute(
        select(Project)
        .options(selectinload(Project.tasks))
        .where(Project.id == project.id)
    )
    project = result.scalars().first()
    return project


async def crud_get_projects(db: AsyncSession, owner_id: str) -> List[Project]:
    query = (
        select(Project)
        .where(Project.owner_id == owner_id)
        .options(
            selectinload(Project.tasks),
            with_loader_criteria(Task, Task.is_completed == False)
        )
    )
    result = await db.execute(query)
    return result.scalars().all()


async def crud_get_project_by_id(db: AsyncSession, project_id: int, owner_id: str) -> Optional[Project]:
    result = await db.execute(
        select(Project)
        .where(Project.id == project_id, Project.owner_id == owner_id)
        .options(selectinload(Project.tasks))
    )
    return result.scalars().first()


async def crud_update_project(db: AsyncSession, project_id: int,
                              user_id: str, project_new: ProjectUpdate) -> Optional[Project]:
    project = await crud_get_project_by_id(db, project_id, user_id)
    if not project:
        return None
    for key, value in project_new.model_dump(exclude_unset=True).items():
        setattr(project, key, value)
    await db.commit()
    await db.refresh(project)
    return project


async def crud_delete_project(db: AsyncSession, project_id: int, user_id: str) -> bool:
    project = await crud_get_project_by_id(db, project_id, user_id)
    if not project:
        return False
    await db.delete(project)
    await db.commit()
    return True