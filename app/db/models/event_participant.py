from app.db.models import Base
from sqlalchemy import Column, Integer, Boolean


class EventParticipant(Base):
    id = Column("event_participant_id", Integer, primary_key=True, autoincrement=True)
    team_id = Column(Integer)
    event_id = Column(Integer, nullable=False)
    confirmed = Column(Boolean, nullable=False)
    user_id = Column(Integer, nullable=False)
