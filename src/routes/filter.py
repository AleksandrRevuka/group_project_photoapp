from typing import List

from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.repository import filter as repository_filter
from src.schemas.filter import PictureFilter, PictureOut, UserFilter, UserOut
from src.services.roles import admin_moderator_user

router = APIRouter(prefix="/search", tags=["search_filter"])


@router.get("/users", dependencies=[Depends(admin_moderator_user)], response_model=List[UserOut])
async def search_users(user_filter: UserFilter = FilterDepends(UserFilter), db: AsyncSession = Depends(get_db)):
    """
    The search_users function searches for users in the database.

    :param user_filter: UserFilter: Define the filter object that will be used to search for users
    :param db: AsyncSession: Get the database session
    :return: A list of users
    """

    users = await repository_filter.search_users(user_filter, db)

    return users


@router.get("/pictures", dependencies=[Depends(admin_moderator_user)], response_model=List[PictureOut])
async def search_pictures(picture_filter: PictureFilter = FilterDepends(PictureFilter), db: AsyncSession = Depends(get_db)):
    """
    The search_pictures function searches for pictures in the database.
        It takes a PictureFilter object as an argument, which is used to filter the search results.
        The function returns a list of PictureOut objects.

    :param picture_filter: PictureFilter: Filter the pictures
    :param db: AsyncSession: Get the database session
    :return: A list of pictures
    """

    pictures = await repository_filter.search_pictures(picture_filter, db)

    return pictures
