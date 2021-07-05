from sqlalchemy.orm import Session
from typing import List

from app.db.repositories.base import BaseRepository
from app.db.models.event_participant import EventParticipant as EventParticipantModel
from app.schemas.event_participant import EventParticipantInDBBase


class EventParticipantRepository(BaseRepository[EventParticipantModel, EventParticipantInDBBase, EventParticipantInDBBase]):
    def get_by_event_id(self, db: Session, event_id: int) -> List[EventParticipantModel]:
        return db.query(self.entity).filter(self.entity.event_id == event_id).all()


event_participant_repository = EventParticipantRepository(EventParticipantModel)
