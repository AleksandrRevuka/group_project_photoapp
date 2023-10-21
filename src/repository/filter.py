from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import Comment, Picture, User
from src.schemas.filter import UserFilter


async def search_users(user_filter: UserFilter, db: AsyncSession):

    query = select(User)\
    .options(selectinload(User.pictures))\
    .options(selectinload(User.comments_user))\
        .join(Comment)\
            .join(Picture)
    query = user_filter.filter(query)
    query = user_filter.sort(query)
    result = (await db.execute(query)).unique()
    users = result.scalars().all()

    return users