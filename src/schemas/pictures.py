from typing import List

from fastapi import File, Query, UploadFile
from pydantic import BaseModel, Field


class TagBase(BaseModel):
    tagname: str


class TagCreate(TagBase):
    pass


class TagDB(TagBase):
    id: int


class PictureBase(BaseModel):
    name: str
    description: str


class PictureUpload(PictureBase):
    tags: List[str] = []


class PydanticFile(BaseModel):
    file: UploadFile = File(...)


class PictureUser(PictureBase):
    id: int
    picture_url: str


class PictureDB(PictureBase):
    id: int
    picture_url: str
    user_id: int


class PictureResponse(BaseModel):
    picture: PictureDB
    detail: str


class PictureNameUpdate(BaseModel):
    name: str


class PictureDescrUpdate(BaseModel):
    description: str


class PictureTransform(BaseModel):
    width: int = Field(ge=0, default=200)
    height: int = Field(ge=0, default=200)
    crop: str = Field(Query(description="'crop' | 'scale' | 'fill' | 'pad' | 'thumb' | 'fit' | 'fill_pad'", default="crop"))
    gravity: str = Field(Query(description="'auto' | 'face' | 'center' | 'north' | 'west' | 'east' | 'south'", default="auto"))
    angle: int = Field(ge=-360, le=360, default=0)
