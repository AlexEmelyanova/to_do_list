from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserRead(UserBase):
    id: UUID
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


