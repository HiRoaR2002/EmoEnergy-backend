from typing import Optional
from pydantic import BaseModel

class ContentBase(BaseModel):
    title: Optional[str] = None
    body: str

class ContentCreate(ContentBase):
    pass

class ContentUpdate(ContentBase):
    summary: Optional[str] = None
    sentiment: Optional[str] = None

class Content(ContentBase):
    id: int
    summary: Optional[str] = None
    sentiment: Optional[str] = None
    owner_id: int

    class Config:
        from_attributes = True
