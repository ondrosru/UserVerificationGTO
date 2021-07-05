from sqlalchemy.orm import Session
from typing import List

from app.db.repositories.base import BaseRepository
from app.db.models.result_on_trial_in_event import ResultOnTrialInEvent as ResultOnTrialInEventModel
from app.schemas.result_on_trial_in_event import ResultOnTrialInEventInDBBase


class ResultOnTrialInEventRepository(BaseRepository[ResultOnTrialInEventModel, ResultOnTrialInEventInDBBase, ResultOnTrialInEventInDBBase]):
    def get_all_by_trial_event_id(self, db: Session, trial_event_id: int) -> List[ResultOnTrialInEventModel]:
        return db.query(self.entity).filter(self.entity.trial_in_event_id == trial_event_id).all()


result_on_trial_in_event_repository = ResultOnTrialInEventRepository(
    ResultOnTrialInEventModel)
