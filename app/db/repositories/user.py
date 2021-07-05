from typing import Optional, List
from sqlalchemy import text as sqlalchemy_text, bindparam
from sqlalchemy.orm import Session

from app.db.repositories.base import BaseRepository
from app.db.models.user import User as UserModel
from app.schemas.user import UserCreate, UserUpdate


class UserRepository(BaseRepository[UserModel, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[UserModel]:
        return db.query(self.entity).filter(self.entity.email == email).first()

    def search_user(self, db: Session, text: str) -> List[UserModel]:
        words = text.split();
        words_for_search = ""
        if words == []:
            return db.query(self.entity).all()
        for word in words:
            words_for_search += "+" + word + "* "
        stmt = sqlalchemy_text("MATCH (name, email) AGAINST(\":value\" IN BOOLEAN MODE)").params(value=words_for_search)
        users = db.query(self.entity).filter(stmt).all()
        return users


user_repository = UserRepository(UserModel)
