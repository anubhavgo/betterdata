from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class RequestLog(BaseModel):
    id: UUID
    method: str
    url: str
    status_code: int
    user_id: str
    created_at: datetime
    
    class Config:
        orm_mode = True