from fastapi import APIRouter
from app.api.v1.endpoints import users, users_photo


api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(users_photo.router, prefix="/user/photos", tags=["User photos"])
