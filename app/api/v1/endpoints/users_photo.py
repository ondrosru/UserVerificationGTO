import os
import shutil
from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
from typing import Any
from datetime import datetime

from app.core.config import get_settings
from app.api.deps import get_db
from app.db.repositories.user import user_repository
from app.db.repositories.user_photo import user_photo_repository
from app.schemas.user_photo import UserPhotoCreate, UserPhotoUpdate


router = APIRouter()
settings = get_settings()
BASE_DIR = os.path.abspath(os.getcwd())


@router.get("/{user_id}")
def get_user_photo(user_id: int,  *, db=Depends(get_db)) -> Any:
    user_photo = user_photo_repository.get_user_photo_by_user_id(db, user_id)
    if not user_photo:
        raise HTTPException(404, detail="User photo not found")
    path = os.path.abspath(os.path.join(BASE_DIR, settings.IMG_DIR, user_photo.img_name))
    if not os.path.exists(path):
        raise HTTPException(404, detail="User photo not found")
    return FileResponse(path)


@router.post("/{user_id}")
def add_user_photo(user_id: int, img: UploadFile = File(...), *, db=Depends(get_db)) -> Any:
    if not user_repository.get(db, id=user_id):
        raise HTTPException(404, detail="User not found")
    user_photo = user_photo_repository.get_user_photo_by_user_id(db, user_id)
    maintype, subtype = img.content_type.split('/')
    if maintype != "image":
        raise HTTPException(400, detail="No image received")
    filename = user_id.__str__() + "_" + datetime.now().strftime("%m_%d_%Y_%H_%M_%S") + "." + subtype
    path = os.path.abspath(os.path.join(BASE_DIR, settings.IMG_DIR, filename))
    with open(path, "wb") as buffer:
        shutil.copyfileobj(img.file, buffer)
    if not user_photo:
        user_photo = user_photo_repository.create(db, obj_in = UserPhotoCreate(
            user_id=user_id,
            img_name=filename,
        ))
    else:
        old_filename_path = os.path.abspath(os.path.join(BASE_DIR, settings.IMG_DIR, user_photo.img_name))
        user_photo = user_photo_repository.update(db, db_obj=user_photo, obj_in=UserPhotoUpdate(
            user_id=user_id,
            img_name=filename,
        ))
        if os.path.exists(old_filename_path):
            os.remove(old_filename_path)
    return user_photo


@router.put("/{id}")
def update_user_photo(id: int, img: UploadFile = File(...), *, db=Depends(get_db)) -> Any:
    user_photo = user_photo_repository.get(db, id)
    if not user_photo:
        raise HTTPException(404, detail="User photo not found")
    maintype, subtype = img.content_type.split('/')
    if maintype != "image":
        raise HTTPException(400, detail="No image received")
    filename = user_photo.user_id.__str__() + "_" + datetime.now().strftime("%m_%d_%Y_%H_%M_%S") + "." + subtype
    path = os.path.abspath(os.path.join(BASE_DIR, settings.IMG_DIR, filename))
    with open(path, "wb") as buffer:
        shutil.copyfileobj(img.file, buffer)
    old_filename_path = path = os.path.abspath(os.path.join(BASE_DIR, settings.IMG_DIR, user_photo.img_name))
    user_photo = user_photo_repository.update(db, db_obj=user_photo, obj_in=UserPhotoUpdate(
        user_id=user_photo.user_id,
        img_name=filename,
    ))
    if os.path.exists(old_filename_path):
        os.remove(old_filename_path)
    return user_photo


@router.delete("/{id}")
def delete_user_photo(id: int, *, db=Depends(get_db)) -> Any:
    user_photo = user_photo_repository.remove(db, id=id)
    if not user_photo:
        raise HTTPException(404, detail="User photo not found")
    path = os.path.abspath(os.path.join(BASE_DIR, settings.IMG_DIR, user_photo.img_name))
    if os.path.exists(path):
        os.remove(path)
    return user_photo
