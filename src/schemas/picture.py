from pydantic import BaseModel


class PictureUpload(BaseModel):
    name: str  # photo's name
    description: str

    # class ConfigDict:
    #     from_attributes = True


class PictureDB(BaseModel):
    name: str  # photo's name
    description: str
    picture_url: str

    class ConfigDict:
        from_attributes = True


class PictureResponse(BaseModel):
    picture: PictureDB
    detail: str

    class ConfigDict:
        from_attributes = True






