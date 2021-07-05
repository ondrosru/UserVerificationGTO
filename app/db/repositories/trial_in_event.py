from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List

from app.db.repositories.base import BaseRepository
from app.db.models.trial_in_event import TrialInEvent as TrialInEventModel
from app.schemas.trial_in_event import TrialInEventInDBBase


class TrialInEventRepository(BaseRepository[TrialInEventModel, TrialInEventInDBBase, TrialInEventInDBBase]):
    def get_all_by_event_id_and_trial_id(self, db: Session, event_id: int, trial_id: int) -> TrialInEventModel:
        return db.query(self.entity).filter(and_(self.entity.event_id == event_id, self.entity.trial_id == trial_id)).first();

    def get_all_by_event_id(self, db: Session, event_id: int) -> List[TrialInEventModel]:
        return db.query(self.entity).filter(self.entity.event_id == event_id).all();


trial_in_event_repository = TrialInEventRepository(TrialInEventModel)