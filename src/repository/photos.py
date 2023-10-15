from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Picture
from src.schemas.photos import PhotoUpload


async def save_data_of_photo_to_db(body: PhotoUpload, picture_url: str, db: AsyncSession):

    photo_datas = Picture(**body.model_dump(), picture_url=picture_url)
    db.add(photo_datas)
    await db.commit()
    await db.refresh(photo_datas)
    return photo_datas
