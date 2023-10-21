from typing import List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends

from src.database.db import get_db
from src.schemas.filter import UserOut, UserFilter
from src.repository import filter as repository_filter
from fastapi_filter import FilterDepends, with_prefix
from fastapi_filter.contrib.sqlalchemy import Filter
from src.database.models import User


router = APIRouter(prefix="/search", tags=["search_filter"])


@router.get("/for_user", response_model=List[UserOut])
async def search_users(user_filter: UserFilter = FilterDepends(UserFilter), 
                       db: AsyncSession = Depends(get_db)):

    users = await repository_filter.search_users(user_filter, db)
    
    return users
