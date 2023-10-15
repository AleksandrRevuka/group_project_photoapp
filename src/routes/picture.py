from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.database.models import User, Picture
from src.schemas.picture import PictureUpload, PictureDb
from src.services.cloud_picture import CloudPicture
from src.services.roles import admin_moderator_user
from src.repository import picture as repository_photos
from src.services.auth import auth_service


router = APIRouter(prefix="/photos", tags=["photos"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(admin_moderator_user)],
    description="User, Moderator and Administrator have access")
async def upload_picture_to_cloudinary(
    body: PictureUpload,
    file: UploadFile = File(),
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db)
):

    public_id = CloudPicture.generate_folder_name(current_user.email)
    r = CloudPicture.upload_picture(file.file, public_id)
    picture_url = CloudPicture.get_url_for_picture(public_id, r)

    photo_datas = await repository_photos.save_data_of_photo_to_db(body, picture_url, db)
    return photo_datas





