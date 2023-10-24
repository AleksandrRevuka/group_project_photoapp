import enum
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

class Crop(enum.Enum):
    none: None = None
    crop: str = "crop"
    scale: str = "scale"
    fill: str = "fill"
    pad: str = "pad"
    thumb: str = "thumb"
    fit: str = "fit"
    fill_pad: str = "fill_pad"
    
class Gravity(enum.Enum):
    none: None = None
    auto: str = "auto"
    face: str = "face"
    center: str = "center"
    north: str = "north"
    west: str = "west"
    east: str = "east"
    south: str = "south"

class Effect(enum.Enum):
    none: None = None
    anti_removal: str = "anti_removal:95"
    bgremoval: str = "bgremoval"
    blackwhite: str = "blackwhite"
    blur_faces: str = "blur_faces:800"
    cartoonify: str = "cartoonify:20:bw"
    
    
class PictureTransform(BaseModel):
    width: int = Field(ge=0, default=800)
    height: int = Field(ge=0, default=800)
    angle: int = Field(ge=-360, le=360, default=0)
    crop: Crop = Crop.none
    gravity: Gravity = Gravity.none
    effect: Effect = Effect.none
