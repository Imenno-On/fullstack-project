from typing import Optional
from pydantic import BaseModel

class TestCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TestUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class TestResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None

    class Config:
        orm_mode = True