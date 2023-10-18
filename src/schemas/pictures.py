from pydantic import BaseModel
from fastapi import File, UploadFile


class TagModel(BaseModel):
    tagname: str


class PictureUpload(BaseModel):
    name: str  # photo's name
    description: str
    tags_picture: list[str]

    class ConfigDict:
        from_attributes = True
        from_dict = True


class PydanticFile(BaseModel):
    file: UploadFile = File(...)


class PictureDB(BaseModel):
    id: int
    name: str  # photo's name
    description: str
    picture_url: str
    user_id: int

    class ConfigDict:
        from_attributes = True


class PictureResponse(BaseModel):
    picture: PictureDB
    detail: str = "The picture was uploaded to the server."

    class ConfigDict:
        from_attributes = True


class PictureNameUpdate(BaseModel):
    name: str  # photo's name


class PictureDescrUpdate(BaseModel):
    description: str  # photo's name
