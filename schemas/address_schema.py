from pydantic import BaseModel

class Address(BaseModel):
    address: str
    city: str
    postal_code: str
    state: str
    primary: bool
    label: str