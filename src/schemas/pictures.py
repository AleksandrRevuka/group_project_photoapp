from pydantic import BaseModel
from fastapi import File, UploadFile


class PictureUpload(BaseModel):
    name: str  # photo's name
    description: str


class PydanticFile(BaseModel):
    file: UploadFile = File(...)


class PictureDB(BaseModel):
    name: str  # photo's name
    description: str
    picture_url: str

    class ConfigDict:
        from_attributes = True


class PictureResponse(BaseModel):
    picture: PictureDB
    detail: str = "The picture was uploaded to the server."


class PictureNameUpdate(BaseModel):
    id: int
    name: str  # photo's name


class PictureDescrUpdate(BaseModel):
    id: int
    description: str  # photo's name
