from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Annotated

from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.crud.task import (
    crud_create_task as crud_create_task,
    crud_complete_task as crud_complete_task,
    crud_delete_task as crud_delete_task,
    crud_update_task as crud_update_task,
    get_completed_tasks as crud_get_completed_tasks,
    crud_get_tasks_by_project as crud_get_tasks_by_project
)
from app.api.deps import get_session, get_current_user
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get(
    "/projects/{project_id}",
    response_model=List[TaskRead],
    summary="Список задач проекта"
)
async def list_tasks_by_project(
    project_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    tasks = await crud_get_tasks_by_project(db, project_id, current_user.id)
    return tasks


@router.get(
    "/completed",
    response_model=List[TaskRead],
    summary="Список выполненных задач"
)
async def read_completed_tasks(
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    tasks = await crud_get_completed_tasks(db, current_user.id)
    return tasks


@router.post(
    "/",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую задачу"
)
async def create_task_endpoint(
    new_task: Annotated[TaskCreate, Body(...)],
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    task = await crud_create_task(db, new_task, current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return task


@router.patch(
    "/{task_id}",
    response_model=TaskRead,
    summary="Обновить задачу"
)
async def update_task_endpoint(
    task_id: int,
    task_update: Annotated[TaskUpdate, Body(...)],
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    task = await crud_update_task(db, task_id, current_user.id, task_update)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.patch(
    "/{task_id}/complete",
    response_model=TaskRead,
    summary="Пометить задачу как выполненную"
)
async def mark_task_complete(
    task_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    task = await crud_complete_task(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить задачу"
)
async def remove_task(
    task_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    success = await crud_delete_task(db, task_id, current_user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return


