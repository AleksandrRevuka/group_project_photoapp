from pydantic import BaseModel
from datetime import datetime

class PictureUpload(BaseModel):
    name: str  # photo's name
    description: str


class PictureDB(BaseModel):
    name: str  # photo's name
    description: str
    picture_url: str
    user_id: int
    

class PictureResponse(BaseModel):
    picture: PictureDB
    detail: str

    class ConfigDict:
        from_attributes = True






