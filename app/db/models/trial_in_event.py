from app.db.models.base import Base
from sqlalchemy import Column, Integer, DateTime


class TrialInEvent(Base):
    id = Column("trial_in_event_id", Integer, primary_key=True, autoincrement=True)
    trial_id = Column(Integer, nullable=False)
    event_id = Column(Integer, nullable=False)
    sport_object_id = Column(Integer, nullable=False)
    start_date_time = Column(DateTime, nullable=False)