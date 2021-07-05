from app.db.models.base import Base
from sqlalchemy import Column, Integer, Enum, String


class ResultOnTrialInEvent(Base):
    id = Column("result_on_trial_in_event_id", Integer, primary_key=True, autoincrement=True)
    badge = Column(Enum("золото", "серебро", "бронза"))
    first_result = Column(String(255))
    second_result = Column(Integer)
    id_result_guide = Column(Integer, nullable=False)
    trial_in_event_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)