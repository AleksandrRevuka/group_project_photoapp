from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Picture
from src.schemas.picture import PictureUpload


async def save_data_of_picture_to_db(body: PictureUpload, picture_url: str, db: AsyncSession):

    picture_datas = Picture(**body.model_dump(), picture_url=picture_url)
    db.add(picture_datas)
    await db.commit()
    await db.refresh(picture_datas)
    return picture_datas
