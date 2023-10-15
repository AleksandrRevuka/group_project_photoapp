from pydantic import BaseModel


class PhotoUpload(BaseModel):
    name: str  # photo's name
    description: str

    class Config:
        from_attributes = True

