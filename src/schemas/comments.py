from pydantic import BaseModel


class CommentCreate(BaseModel):
    user_id: int
    text: str
    picture_id: int


class CommentUpdate(BaseModel):
    text: str
