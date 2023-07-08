from pydantic import BaseModel

class TokenData(BaseModel):
    user_id: str | None = None
    exp: int | None = None