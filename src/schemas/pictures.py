from typing import List
from pydantic import BaseModel, Field
from fastapi import File, UploadFile


class TagBase(BaseModel):
    tagname: str


class TagCreate(TagBase):
    pass


class TagDB(TagBase):
    id: int

    # class ConfigDict:
    #     from_attributes = True


class PictureBase(BaseModel):
    name: str  # picture's name
    description: str


class PictureUpload(PictureBase):
    tags: List[str] = []


class PydanticFile(BaseModel):
    file: UploadFile = File(...)


class PictureDB(PictureBase):
    id: int
    picture_url: str
    user_id: int
    # tags_picture: List[TagDB] = []

    # class ConfigDict:
    #     from_attributes = True


class PictureResponse(BaseModel):
    picture: PictureDB
    detail: str

    # class ConfigDict:
    #     from_attributes = True


class PictureNameUpdate(BaseModel):
    name: str  # picture's name


class PictureDescrUpdate(BaseModel):
    description: str  # picture's name


class PictureTransform(BaseModel):
    width: int = Field(ge=0, default=200)
    height: int = Field(ge=0, default=200)
    crop: str = "crop"  # 'crop'|'scale'|'fill'|'pad'|'thumb'|'fit'|'fill_pad'
    gravity: str = "auto"  # 'auto'|'face'|'center'|'north'|'west'|'east'|'south'
    angle: int = Field(ge=-360, le=360, default=0)
