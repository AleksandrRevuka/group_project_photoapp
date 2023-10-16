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

