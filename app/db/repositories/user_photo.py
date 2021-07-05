from sqlalchemy.orm import Session
from typing import Optional

from app.db.repositories.base import BaseRepository
from app.db.models.user_photo import UserPhoto as UserPhotoModel
from app.schemas.user_photo import UserPhotoCreate, UserPhotoUpdate


class UserPhotoRepository(BaseRepository[UserPhotoModel, UserPhotoCreate, UserPhotoUpdate]):
    def get_user_photo_by_user_id(self, db: Session, user_id: int) -> Optional[UserPhotoModel]:
        return db.query(self.entity).filter(self.entity.user_id == user_id).first()


user_photo_repository = UserPhotoRepository(UserPhotoModel)
