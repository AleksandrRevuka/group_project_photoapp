from pydantic import BaseModel


class CommentCreate(BaseModel):
    text: str


class CommentUpdate(BaseModel):
    text: str
