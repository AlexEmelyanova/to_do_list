from typing import List, Annotated

from fastapi import APIRouter, HTTPException, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from app.api.deps import get_current_user
from app.core.database import get_session
from app.crud.project import crud_create_project, crud_get_projects, crud_get_project_by_id, crud_update_project, crud_delete_project
from app.models import User
from app.schemas.project import ProjectRead, ProjectCreate, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("/", response_model=List[ProjectRead], summary="Получить список проектов пользователя")
async def list_of_projects(
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    projects = await crud_get_projects(db, current_user.id)
    return projects


@router.get("/{project_id}", response_model=ProjectRead, summary="Получить проект по ID")
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    project = await crud_get_project_by_id(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.post("/", response_model=ProjectRead, status_code=HTTP_201_CREATED, summary="Создать новый проект")
async def create_new_project(
    new_project: Annotated[ProjectCreate, Body(...)],
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    project = await crud_create_project(db, new_project, current_user.id)
    return project


@router.patch("/{project_id}", response_model=ProjectRead, summary="Обновить проект")
async def update_project_route(
    project_id: int,
    project_in: Annotated[ProjectUpdate, Body(...)],
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    project = await crud_update_project(db, project_id, current_user.id, project_in)
    if not project:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.delete("/{project_id}", status_code=HTTP_204_NO_CONTENT, summary="Удалить проект")
async def delete_project_route(
    project_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    success = await crud_delete_project(db, project_id, current_user.id)
    if not success:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Project not found")
    return