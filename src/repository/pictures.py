from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import join, outerjoin, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Picture, Role, Tag, User, picture_tags
from src.schemas.filters import PictureFilter
from src.schemas.pictures import (PictureDescrUpdate, PictureNameUpdate,
                                  PictureUpload)
from src.services.qrcode_generator import qrcode_generator
from src.conf.messages import messages


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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.get_message("PICTURE_NOT_FOUND"))

    if body.name == "":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=messages.get_message("NAME_OF_PICTURE_CANT_BE_EMPTY"),
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.get_message("PICTURE_NOT_FOUND"))

    if body.description == "":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=messages.get_message("DESCRIPTION_OF_PICTURE_CANT_BE_EMPTY"),
        )

    picture_descr.description = body.description
    db.add(picture_descr)
    await db.commit()
    await db.refresh(picture_descr)
    return picture_descr


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


async def retrieve_tags_for_picture(picture_id: int, db: AsyncSession):
    """
    The retrieve_tags_for_picture function takes in a picture_id and an AsyncSession object.
    It then uses the given session to execute a query that joins the Tag, Picture, and picture_tags tables together.
    The function returns all of the tags associated with the given picture.

    :param picture_id: int: Specify the picture to retrieve tags for
    :param db: AsyncSession: Pass the database session to the function
    :return: A list of tags for a given picture
    """

    picture = await db.scalar(select(Picture).filter(Picture.id == picture_id))
    if picture:
        tags = [tag for tag in await picture.awaitable_attrs.tags_picture]
        
    return tags

async def search_pictures(picture_filter: PictureFilter, db: AsyncSession):
    """
    The search_pictures function takes a PictureFilter object and an AsyncSession object as arguments.
    The function then creates a query that selects all pictures, joins them with their tags, and loads the comments_picture,
    tags_picture, and ratings attributes of each picture. The query is then filtered by the filter method of the PictureFilter
    object passed to it as an argument. Finally, the sort method of this same PictureFilter object is called on this query to
    sort it in some way (if applicable). The result is returned.

    :param picture_filter: PictureFilter: Filter the pictures
    :param db: AsyncSession: Pass the database session to the function
    :return: A list of picture objects
    """

    query = (
        select(Picture)
        .select_from(outerjoin(Picture, picture_tags.join(Tag)))
        .options(selectinload(Picture.comments_picture))
        .options(selectinload(Picture.tags_picture))
        .options(selectinload(Picture.ratings))
    )

    query = picture_filter.filter(query)
    query = picture_filter.sort(query)
    result = (await db.execute(query)).unique()
    return result.scalars().all()