from datetime import datetime

from pydantic import BaseModel


class TagModel(BaseModel):
    tagname: str


class TagResponse(BaseModel):
    id: int
    tagname: str
    created_at: datetime
    updated_at: datetime
