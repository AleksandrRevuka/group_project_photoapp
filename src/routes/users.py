
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from src.conf.config import init_async_redis
from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.schemas.user import UserDb, UserResponse
from src.services.auth import auth_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/", response_model=UserDb)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user),
                        redis_client: Redis = Depends(init_async_redis)) -> User:
    """
    The read_users_me function is a GET endpoint that returns the current user's information.

    :param current_user: User: Get the current user from the database
    :return: The current user object
    """
    key_to_clear = f"user:{current_user.email}"
    await redis_client.delete(key_to_clear)
    return current_user


@router.patch("/edit_my_profile", response_model=UserResponse)
async def edit_my_profile(
    name: str,
    file: UploadFile = File(),
    current_user: User = Depends(auth_service.get_current_user), 
    db: AsyncSession = Depends(get_db)
) -> dict:
    user_exist = await repository_users.get_user_username(name, db)
    
    if user_exist:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this name aready exists!")
     
    user = await repository_users.edit_my_profile(current_user.email, file, name, db)
    
    
    return {"user": user, "detail": "My profile was successfully edited"}
