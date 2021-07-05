from app.db.models.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class UserPhoto(Base):
    id = Column("user_photo_id", Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    img_name = Column(String(100), nullable=False)
    user = relationship("User", back_populates="photos")
