from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Picture, User
from src.schemas.pictures import PictureNameUpdate, PictureDescrUpdate
from fastapi import HTTPException, status
from sqlalchemy import select


async def save_data_of_picture_to_db(
    name: str, description: str, picture_url: str, user: User, db: AsyncSession
):
    """
    The save_data_of_picture_to_db function saves the data of a picture to the database.
        Args:
            name (str): The name of the picture.
            description (str): The description of the picture.
            picture_url (str): The url where you can find this image on your server or online somewhere else.

    :param name: str: Give the picture a name
    :param description: str: Get the description of the picture
    :param picture_url: str: Store the picture url in the database
    :param user: User: Get the id of the user that is logged in
    :param db: AsyncSession: Create a connection to the database
    :return: The picture data
    """

    picture_datas = Picture(
        name=name, description=description, picture_url=picture_url, user_id=user.id
    )
    db.add(picture_datas)
    await db.commit()
    await db.refresh(picture_datas)
    return picture_datas


async def update_picture_name(
    id: int, body: PictureNameUpdate, db: AsyncSession
) -> Picture:
    """
    The update_picture_name function updates the name of a picture in the database.
        Args:
            id (int): The ID of the picture to update.
            body (PictureNameUpdate): The new name for this picture.

    :param id: int: Get the id of the picture we want to update
    :param body: PictureNameUpdate: Get the new name of picture
    :param db: AsyncSession: Pass the database session to the function
    :return: A picture with a new name
    """

    picture_query = select(Picture).where(Picture.id == id)
    existing_name = await db.execute(picture_query)
    picture_name = existing_name.scalar()
    if not picture_name:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Picture is not found"
        )

    # Перевірка того, що коментар не порожній
    if body.name == "":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Name of picture can't be empty",
        )
    # Перезаписуємо коментар з новими даними
    picture_name.name = body.name
    db.add(picture_name)
    await db.commit()
    await db.refresh(picture_name)
    return picture_name


async def update_picture_description(
    id: int, body: PictureDescrUpdate, db: AsyncSession
) -> Picture:
    """
    The update_picture_description function updates the description of a picture.
        Args:
            id (int): The ID of the picture to update.
            body (PictureDescrUpdate): The updated description for the picture.

    :param id: int: Specify the id of the picture whose description we want to update
    :param body: PictureDescrUpdate: Get the new description of the picture
    :param db: AsyncSession: Access the database
    :return: A picture object
    """

    picture_query = select(Picture).where(Picture.id == id)
    existing_descr = await db.execute(picture_query)
    picture_descr = existing_descr.scalar()
    if not picture_descr:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Picture is not found"
        )

    # Перевірка того, що коментар не порожній
    if body.description == "":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Name of picture can't be empty",
        )
    # Перезаписуємо коментар з новими даними
    picture_descr.description = body.description
    db.add(picture_descr)
    await db.commit()
    await db.refresh(picture_descr)
    return picture_descr


async def get_all_pictures(
    skip: int, limit: int, db: AsyncSession
) -> Sequence[Picture]:
    """
    The get_all_pictures function returns a list of all pictures in the database.
        ---
        get:
          summary: Get all pictures from the database.
          description: Returns a list of all pictures in the database, with optional pagination parameters.

    :param skip: int: Skip a certain amount of pictures
    :param limit: int: Limit the number of pictures that are returned
    :param db: AsyncSession: Pass the database session into the function
    :return: A list of picture objects
    """

    query = select(Picture).offset(skip).limit(limit)
    pictures = await db.execute(query)
    result = pictures.scalars().all()
    return result


async def get_picture_by_id(id: int, db: AsyncSession) -> Sequence[Picture]:
    """
    The get_picture_by_id function takes in an id and a database session,
        and returns the picture with that id.

    :param id: int: Specify the id of the picture we want to get from the database
    :param db: AsyncSession: Pass the database session to the function
    :return: A list of pictures with the given id
    """

    query = select(Picture).where(Picture.id == id)
    picture = await db.execute(query)
    result = picture.scalars().all()
    return result


async def get_all_pictures_of_user(
    user_id: int, skip: int, limit: int, db: AsyncSession
) -> Sequence[Picture]:
    """
    The get_all_pictures_of_user function returns a list of all pictures that belong to the user with the given id.
    The function takes in three arguments:
        - user_id: The id of the user whose pictures we want to retrieve.
        - skip: The number of records we want to skip before returning results (useful for pagination).
        - limit: The maximum number of records we want returned (useful for pagination).

    :param user_id: int: Identify the user
    :param skip: int: Skip a certain amount of pictures
    :param limit: int: Limit the number of pictures returned
    :param db: AsyncSession: Pass the database session to the function
    :return: A list of pictures
    """

    query = select(Picture).where(Picture.user_id == user_id).offset(skip).limit(limit)
    pictures = await db.execute(query)
    result = pictures.scalars().all()
    return result



async def remove_picture(picture_id: int, current_user: User, db: AsyncSession):
    """
    The remove_picture function removes a picture from the database.
        It takes in a picture_id and current_user, which are used to find the correct picture to remove.
        The function returns None if no such user exists or if the user is not authorized to delete this image.
    
    :param picture_id: int: Find the picture in the database
    :param current_user: User: Check if the user is allowed to delete the picture
    :param db: AsyncSession: Pass the database session to the function
    :return: A picture object
    """

    query = select(Picture).where(Picture.id == picture_id)
    picture = await db.execute(query)
    result = picture.scalars().first()

    if result is None:
        return None
    
    if current_user.roles == 'admin' or result.user_id == current_user.id:
        await db.delete(result)
        await db.commit()
        return result
    else:
        return None