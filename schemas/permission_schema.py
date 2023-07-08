from typing import List
from pydantic import BaseModel

class Permission(BaseModel):
    id: int
    description: str