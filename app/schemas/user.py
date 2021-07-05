from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    uid: Optional[str]
    name: str
    email: Optional[EmailStr] = None
    date_of_birth: datetime
    role_id: int
    gender: int
    is_activity: bool


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    password: str


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass
