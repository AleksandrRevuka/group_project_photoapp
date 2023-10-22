from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Picture, Role, Tag, User
from src.schemas.pictures import (PictureDescrUpdate, PictureNameUpdate,
                                  PictureUpload)
from src.services.qrcode_generator import qrcode_generator


async def save_data_of_picture_to_db(body: PictureUpload, picture_url: str, user: User, db: AsyncSession, tag_names: list):
    """
    The save_data_of_picture_to_db function saves the data of a picture to the database.

    :param body: PictureUpload: Get the name and description of the picture
    :param picture_url: str: Save the url of the picture in the database
    :param tag_names: list: Get the list of tags that are associated with a picture
    :param user: User: Get the user_id of the picture
    :param db: AsyncSession: Make sure that the function is able to access the database
    :return: A picture object
    """
    tags = []
    if tag_names:
        for tag_name in tag_names:
            tag = await get_or_create_tag(db, tag_name)
            tags.append(tag)

    picture_data = Picture(
        name=body.name, description=body.description, picture_url=picture_url, user_id=user.id, tags_picture=tags
    )
    db.add(picture_data)
    await db.commit()
    await db.refresh(picture_data)

    return picture_data


async def get_or_create_tag(db: AsyncSession, tag_name: str) -> Tag:
    """
    The get_or_create_tag function takes a database session and a tag name as arguments.
    It then queries the database for an existing tag with that name, returning it if found.
    If no such tag exists, it creates one and returns that instead.

    :param db: AsyncSession: Pass in the database connection
    :param tag_name: str: Specify the name of the tag that we want to create or retrieve
    :return: A tag object
    """
    query = select(Tag).where(Tag.tagname == tag_name)
    existing_tag = await db.execute(query)
    tag = existing_tag.scalar_one_or_none()

    if not tag:
        tag = Tag(tagname=tag_name)
        db.add(tag)
        await db.commit()
        return tag

    return tag


async def update_picture_name(id: int, body: PictureNameUpdate, current_user: int, db: AsyncSession) -> Picture:
    """
    The update_picture_name function updates the name of a picture.
        Args:
            id (int): The ID of the picture to update.
            body (PictureNameUpdate): The new name for the picture.

    :param id: int: Get the picture id
    :param body: PictureNameUpdate: Update the name of a picture
    :param current_user: int: Check if the user is authorized to delete a picture
    :param db: AsyncSession: Access the database
    :return: The updated picture name
    """

    picture_query = select(Picture).where(Picture.id == id, Picture.user_id == current_user)
    existing_name = await db.execute(picture_query)
    picture_name = existing_name.scalar()
    if not picture_name:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Picture is not found")

    if body.name == "":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Name of picture can't be empty",
        )

    picture_name.name = body.name
    db.add(picture_name)
    await db.commit()
    await db.refresh(picture_name)
    return picture_name


async def update_picture_description(id: int, body: PictureDescrUpdate, current_user: int, db: AsyncSession) -> Picture:
    """
    The update_picture_description function updates the description of a picture.

    :param id: int: Get the id of a picture
    :param body: PictureDescrUpdate: Get the new description of picture
    :param current_user: int: Check that the user is authorized to make changes
    :param db: AsyncSession: Access the database
    :return: The updated picture
    """

    picture_query = select(Picture).where(Picture.id == id, Picture.user_id == current_user)
    existing_descr = await db.execute(picture_query)
    picture_descr = existing_descr.scalar()
    if not picture_descr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Picture is not found")

    if body.description == "":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Description of picture can't be empty",
        )

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


async def remove_picture(picture_id: int, current_user: User, db: AsyncSession):
    """
    The remove_picture function is used to remove a picture from the database.
    It takes in a picture_id and current_user as parameters, and returns the removed
    picture if successful. If not successful, it returns None.

    :param picture_id: int: Identify the picture to be removed
    :param current_user: User: Check if the user is an admin or not
    :param db: AsyncSession: Pass the database session to the function
    :return: The picture that was deleted, if it exists
    """

    query = select(Picture).where(Picture.id == picture_id)
    picture = await db.execute(query)
    result = picture.scalars().first()

    if result is None:
        return None

    if current_user.roles == Role.admin or result.user_id == current_user.id:
        await db.delete(result)
        await db.commit()
        return result
    else:
        return None


async def get_qrcode(picture_id: int, db: AsyncSession):
    """
    The get_qrcode function takes in a picture_id and returns the qrcode for that picture.
        If no such picture exists, it returns None.

    :param picture_id: int: Specify the id of the picture
    :param db: AsyncSession: Pass the database session into the function
    :return: A qrcode object
    :doc-author: Trelent
    """
    query = select(Picture).where(Picture.id == picture_id)
    picture = await db.execute(query)
    result = picture.scalars().first()

    if result is None:
        return None

    return qrcode_generator.generate_qrcode(result.picture_url)
