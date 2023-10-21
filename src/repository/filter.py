from sqlalchemy import join, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import Comment, Picture, Tag, User, picture_tags
from src.schemas.filter import PictureFilter, UserFilter


async def search_users(user_filter: UserFilter, db: AsyncSession):
    """
    The search_users function takes in a UserFilter object and an AsyncSession object.
    The function then creates a query that selects all users, with their pictures, comments_user, and ratings loaded.
    It joins the Comment table to the User table. The user_filter is used to filter the query by its filter method.
    The user_filter is also used to sort the query by its sort method.

    :param user_filter: UserFilter: Filter the users by their attributes
    :param db: AsyncSession: Pass in the database session
    :return: A list of users
    """

    query = (
        select(User)
        .options(selectinload(User.pictures))
        .options(selectinload(User.comments_user))
        .options(selectinload(User.ratings))
        .join(Comment)
    )
    query = user_filter.filter(query)

    query = user_filter.sort(query)
    result = (await db.execute(query)).unique()
    users = result.scalars().all()

    return users


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
        .select_from(join(Picture, picture_tags.join(Tag)))
        .options(selectinload(Picture.comments_picture))
        .options(selectinload(Picture.tags_picture))
        .options(selectinload(Picture.ratings))
    )

    query = picture_filter.filter(query)
    query = picture_filter.sort(query)

    result = (await db.execute(query)).unique()
    return result.scalars().all()
