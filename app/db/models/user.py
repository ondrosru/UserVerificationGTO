from app.db.models.base import Base
from sqlalchemy import Column, Boolean, Integer, String, Date, DateTime, func
from sqlalchemy.orm import relationship


class User(Base):
    __searchable__=["name", "email"]
    id = Column("user_id", Integer, primary_key=True, autoincrement=True)
    uid = Column(String(20))
    name = Column(String(255), nullable=False)
    password = Column(String(1000), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    role_id = Column(Integer, nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    gender = Column(Integer, nullable=False)
    is_activity = Column(Boolean, default=True, nullable=False)
    registration_date = Column(Date, default=func.now(), nullable=False)
    photos = relationship("UserPhoto", back_populates="user")
