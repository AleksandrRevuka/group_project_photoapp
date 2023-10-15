from pydantic import BaseModel


class PictureUpload(BaseModel):
    name: str  # photo's name
    description: str

    # class ConfigDict:
    #     from_attributes = True


class PictureDb(BaseModel):
    name: str  # photo's name
    description: str
    picture_url: str

    # class ConfigDict:
    #     from_attributes = True



