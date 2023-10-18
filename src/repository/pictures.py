from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Picture, User, Tag
from src.schemas.pictures import PictureNameUpdate, PictureDescrUpdate, PictureUpload
from fastapi import HTTPException, status
from sqlalchemy import select


async def save_data_of_picture_to_db(body: PictureUpload, picture_url: str, tag_names: list, user: User, db: AsyncSession):
    tags = [Tag(tagname=tag_name) for tag_name in tag_names]

    for tag in tags:
        db.add(tag)

    await db.commit()

    picture_data = Picture(
        name=body.name, description=body.description, picture_url=picture_url, user_id=user.id, tags_picture=tags
    )
    db.add(picture_data)
    await db.commit()
    await db.refresh(picture_data)
    return picture_data


async def update_picture_name(id: int, body: PictureNameUpdate, db: AsyncSession) -> Picture:
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Picture is not found")

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


async def update_picture_description(id: int, body: PictureDescrUpdate, db: AsyncSession) -> Picture:
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Picture is not found")

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


async def get_all_pictures(skip: int, limit: int, db: AsyncSession) -> Sequence[Picture]:
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


async def get_all_pictures_of_user(user_id: int, skip: int, limit: int, db: AsyncSession) -> Sequence[Picture]:
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
