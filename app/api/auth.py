from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_cloud_cli.commands.login import TokenResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_409_CONFLICT
from app.crud.user import get_user_by_email, crud_create_user
from app.schemas.user import UserCreate, UserRead
from app.core.database import get_session
from app.core.security import create_access_token, verify_password


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserRead,
    summary="Регистрация нового пользователя",
    status_code=status.HTTP_201_CREATED
)
async def register(
    new_user: Annotated[UserCreate, Body(...)],
    db: AsyncSession = Depends(get_session)
):
    existing_user = await get_user_by_email(db, new_user.email)
    if existing_user:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail="User already exists")
    user = await crud_create_user(db, new_user)
    return user

@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Авторизация пользователя"
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session)
):
    user = await get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(str(user.id))
    return {"access_token": token, "token_type": "bearer"}