from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.database.models import User
from src.schemas.photos import PhotoUpload, PhotoDb
from src.services.cloud_image import CloudImage
from src.services.roles import admin_moderator_user
from src.repository import photos as repository_photos
from src.services.auth import auth_service


router = APIRouter(prefix="/photos", tags=["photos"])


@router.post(
    "/",
    response_model=PhotoDb,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(admin_moderator_user)],
    description="User, Moderator and Administrator have access",
)
async def upload_photo_to_cloudinary(
    body: PhotoUpload,
    file: UploadFile = File(),
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
):

    public_id = CloudImage.generate_folder_name(current_user.email)
    r = CloudImage.upload_image(file.file, public_id)
    picture_url = CloudImage.get_url_for_image(public_id, r)

    photo_datas = await repository_photos.save_data_of_photo_to_db(body, picture_url, db)
    return photo_datas





