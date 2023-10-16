from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File

from src.database.db import get_db
from src.database.models import User
from src.schemas.pictures import (
    PictureUpload,
    PictureResponse,
    PictureNameUpdate,
    PictureDescrUpdate,
)
from src.services.cloud_picture import CloudPicture
from src.services.roles import admin_moderator_user
from src.repository import pictures as repository_pictures
from src.services.auth import auth_service

router = APIRouter(prefix="/pictures", tags=["pictures"])


@router.post(
    "/",
    response_model=PictureResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(admin_moderator_user)],
    description="User, Moderator and Administrator have access",
)
async def upload_picture_to_cloudinary(
    body: PictureUpload = Depends(),
    file: UploadFile = File(...),
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    The upload_picture_to_cloudinary function uploads a picture to the cloudinary server.
        The function takes in a body, file, current_user and db as parameters.
        The body is of type PictureUpload which contains the name and description of the picture being uploaded.
        The file is an UploadFile object that contains information about the actual image being uploaded to Cloudinary.
            This includes things like its size, content-type etc...
            It also has an attribute called 'file' which points to a BytesIO object containing all of our image data (the raw bytes).

    :param body: PictureUpload: Get the name and description of the picture
    :param file: UploadFile: Receive the file sent by the client
    :param current_user: User: Get the user that is currently logged in
    :param db: AsyncSession: Get the database session
    :return: A dictionary with the picture and a detail message
    """

    public_id = CloudPicture.generate_folder_name(current_user.email)
    r = CloudPicture.upload_picture(file.file, public_id)
    picture_url = CloudPicture.get_url_for_picture(public_id, r)

    picture_datas = await repository_pictures.save_data_of_picture_to_db(
        body.name, body.description, picture_url, current_user, db
    )
    return {
        "picture": picture_datas,
        "detail": "The picture was uploaded to the server.",
    }


@router.put(
    "/{body.picture_id}",
    dependencies=[Depends(admin_moderator_user)],
    description="User, Moderator and Administrator have access",
)
async def update_name_of_picture(
    body: PictureNameUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    The update_name_of_picture function updates the name of a picture.
        The function takes in a PictureNameUpdate object, which contains the id of the picture to be updated and its new name.
        It then uses this information to update the database with an UPDATE query.

    :param body: PictureNameUpdate: Get the new name of the picture from the request body
    :param db: AsyncSession: Get the database session
    :param : Get the picture id from the url
    :return: An updated picture name
    """

    updated_name = await repository_pictures.update_picture_name(body, db)
    if updated_name is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment has been not updated"
        )
    return updated_name


@router.put(
    "/{body.description}",
    dependencies=[Depends(admin_moderator_user)],
    description="User, Moderator and Administrator have access",
)
async def update_description_of_picture(
    body: PictureDescrUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    The update_description_of_picture function updates the description of a picture.
        The function takes in a PictureDescrUpdate object and returns an updated Picture object.

    :param body: PictureDescrUpdate: Get the data from the request body
    :param db: AsyncSession: Get the database session
    :param : Get the picture id
    :return: The updated description of the picture
    :doc-author: Trelent
    """
    updated_descr = await repository_pictures.update_picture_description(body, db)
    if updated_descr is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Description has been not updated",
        )
    return updated_descr
