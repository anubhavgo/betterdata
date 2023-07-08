from typing import List
from pydantic import BaseModel

class Role(BaseModel):
    id: str
    name: str