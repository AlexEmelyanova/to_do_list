from typing import Optional, Type, Sequence, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Task, Project
from app.schemas.task import TaskCreate, TaskUpdate


async def crud_create_task(db: AsyncSession, new_task: TaskCreate, user_id: str) -> Task:
    result = await db.execute(
        select(Project).where(
            Project.id == new_task.project_id,
            Project.owner_id == user_id
        )
    )
    project = result.scalar_one_or_none()

    if not project:
        return None

    task = Task(**new_task.model_dump())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def crud_get_user_task(db: AsyncSession, task_id: int, user_id: str) -> Optional[Task]:

    result = await db.execute(
        select(Task)
        .join(Project)
        .where(
            Task.id == task_id,
            Project.owner_id == user_id
        )
    )

    return result.scalar_one_or_none()


async def crud_get_tasks_by_project(db: AsyncSession, project_id: int, user_id: str) -> list[Task]:

    result = await db.execute(
        select(Task)
        .join(Project)
        .where(Task.project_id == project_id, Project.owner_id == user_id)
        .where(Task.is_completed == False)
    )

    return result.scalars().all()


async def crud_complete_task(db: AsyncSession, task_id: int, user_id: str) -> Optional[Task]:
    task = await crud_get_user_task(db, task_id, user_id)
    if not task:
        return None

    task.is_completed = True
    await db.commit()
    await db.refresh(task)
    return task


async def crud_delete_task(db: AsyncSession, task_id: int, user_id: str) -> bool:
    task = await crud_get_user_task(db, task_id, user_id)
    if not task:
        return False

    await db.delete(task)
    await db.commit()
    return True



async def crud_update_task(db: AsyncSession, task_id: int, user_id: str, task_update: TaskUpdate) -> Optional[Task]:
    task = await crud_get_user_task(db, task_id, user_id)
    if not task:
        return None

    update_data = task_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(task, field, value)

    await db.commit()
    await db.refresh(task)

    return task


async def get_completed_tasks(db: AsyncSession, user_id: str) -> List[Task]:
    tasks = await db.execute(
        select(Task)
        .join(Project)
        .where(Project.owner_id == user_id)
        .where(Task.is_completed == True)
    )
    return tasks.scalars().all()
