from pydantic import BaseModel


class TrialInEventInDBBase(BaseModel):
    class Config:
        orm_mode = True
