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


@router.patch(
    "/picture/{picture_id}",
    dependencies=[Depends(admin_moderator_user)],
    description="User, Moderator and Administrator have access",
)
async def update_name_of_picture(
    id: int,
    body: PictureNameUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    The update_name_of_picture function updates the name of a picture in the database.
        The function takes an id and body as input, and returns an updated picture object.

    :param id: int: Get the id of the picture that we want to update
    :param body: PictureNameUpdate: Get the new name of the picture from the request body
    :param db: AsyncSession: Pass a database session to the function
    :param : Get the id of the picture to be updated
    :return: The updated picture name
    """

    updated_name = await repository_pictures.update_picture_name(id, body, db)
    if updated_name is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment has been not updated"
        )
    return updated_name


@router.patch(
    "/description/{description}",
    dependencies=[Depends(admin_moderator_user)],
    description="User, Moderator and Administrator have access",
)
async def update_description_of_picture(
    id: int,
    body: PictureDescrUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    The update_description_of_picture function updates the description of a picture.
        The function takes in an id and body, which is a PictureDescrUpdate object.
        It then uses the repository_pictures module to update the description of that picture in our database.


    :param id: int: Identify the picture to update
    :param body: PictureDescrUpdate: Pass the new description of a picture
    :param db: AsyncSession: Get the database session
    :param : Get the id of the picture
    :return: A picturedescrupdate object
    """

    updated_descr = await repository_pictures.update_picture_description(id, body, db)
    if updated_descr is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Description has been not updated",
        )
    return updated_descr


@router.get(
    "/picture/all_pictures",
    dependencies=[Depends(admin_moderator_user)],
    description="User, Moderator and Administrator have access",
)
async def get_all_pictures(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    """
    The get_all_pictures function returns a list of all pictures in the database.
    The skip and limit parameters are used to paginate the results.

    :param skip: int: Skip a number of pictures from the database
    :param limit: int: Limit the number of pictures returned
    :param db: AsyncSession: Get the database session
    :param : Get the picture by id
    :return: A list of pictures
    """

    pictures = await repository_pictures.get_all_pictures(skip, limit, db)
    if not pictures:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pictures not found"
        )
    return pictures


@router.get(
    "/picture/{id}",
    dependencies=[Depends(admin_moderator_user)],
    description="User, Moderator and Administrator have access",
)
async def get_picture_by_id(
    id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    The get_picture_by_id function returns a picture by its id.
        If the picture does not exist, it raises an HTTP 404 error.

    :param id: int: Specify the id of the picture to be returned
    :param db: AsyncSession: Pass the database connection to the function
    :param : Get the picture by id
    :return: A single picture
    """

    pictures = await repository_pictures.get_picture_by_id(id, db)
    if not pictures:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Picture not found"
        )
    return pictures


@router.get(
    "/all_pictures/{user_id}",
    dependencies=[Depends(admin_moderator_user)],
    description="User, Moderator and Administrator have access",
)
async def get_all_pictures_of_user(
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    """
    The get_all_pictures_of_user function returns all pictures of a user.

    :param user_id: int: Get all the pictures of a specific user
    :param skip: int: Skip the first n pictures
    :param limit: int: Limit the number of pictures returned
    :param db: AsyncSession: Pass the database session to the repository layer
    :param : Get the user id of the user that is logged in
    :return: A list of pictures
    """

    pictures = await repository_pictures.get_all_pictures_of_user(
        user_id, skip, limit, db
    )
    if not pictures:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pictures of this user not found",
        )
    return pictures



@router.delete(
    "/all_pictures/{picture_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_picture(
    picture_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
):
    """
    The delete_picture function deletes a picture from the database.
    
    :param picture_id: int: Identify the picture to delete
    :param db: AsyncSession: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: The deleted picture
    :doc-author: Trelent
    """
    picture = await repository_pictures.remove_picture(picture_id, current_user, db)
    
    if picture is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Picture not found")

    return picture

