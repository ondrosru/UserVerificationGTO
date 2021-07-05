from typing import Optional
from pydantic import BaseModel


class UserPhotoBase(BaseModel):
    user_id: int
    img_name: Optional[str]


class UserPhotoCreate(UserPhotoBase):
    img_name: str


class UserPhotoUpdate(UserPhotoBase):
    img_name: str


class UserPhotoInDBBase(UserPhotoBase):
    id: int

    class Config:
        orm_mode = True


class UserPhoto(UserPhotoInDBBase):
    pass
