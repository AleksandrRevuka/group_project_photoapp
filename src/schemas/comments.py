from pydantic import BaseModel, ConfigDict


class CommentCreate(BaseModel):
    text: str


class CommentUpdate(CommentCreate):
    pass

class CommentDB(CommentCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    text: str
    user_id: int