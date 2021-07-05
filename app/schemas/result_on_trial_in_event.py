from pydantic import BaseModel

class ResultOnTrialInEventInDBBase(BaseModel):
    class Config:
        orm_mode = True
