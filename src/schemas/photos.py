from pydantic import BaseModel


class PhotoUpload(BaseModel):
    name: str  # photo's name
    description: str

    class Config:
        from_attributes = True


class PhotoDb(BaseModel):
    name: str  # photo's name
    description: str
    picture_url: str

    class Config:
        from_attributes = True



