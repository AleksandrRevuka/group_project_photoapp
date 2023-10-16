from pydantic import BaseModel
from fastapi import File, UploadFile


class PictureUpload(BaseModel):
    name: str  # photo's name
    description: str


class PydanticFile(BaseModel):
    file: UploadFile = File(...)


class PictureDB(BaseModel):
    id: int
    name: str  # photo's name
    description: str
    picture_url: str
    user_id: int


class PictureResponse(BaseModel):
    picture: PictureDB
    detail: str = "The picture was uploaded to the server."


class PictureNameUpdate(BaseModel):
    name: str  # photo's name


class PictureDescrUpdate(BaseModel):
    description: str  # photo's name
