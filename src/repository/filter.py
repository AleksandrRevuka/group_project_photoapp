from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Comment, Picture, User
from src.schemas.filter import UserFilter


async def search_users(user_filter: UserFilter, db: AsyncSession):
    query = select(User)
    query = user_filter.filter(query)
    result = await db.execute(query)
    users = result.scalars().all()
    return users