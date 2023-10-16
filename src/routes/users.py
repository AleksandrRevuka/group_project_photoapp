
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from src.conf.config import init_async_redis
from src.database.db import get_db
from src.database.models import User, Role
from src.repository import users as repository_users
from src.schemas.user import UserDb, UserResponse, UserProfile
from src.services.auth import auth_service
from src.services.roles import admin, admin_moderator

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
    """
    The edit_my_profile function allows a user to edit their profile.
        The function takes in the following parameters:
            name (str): The new username of the user.
            file (UploadFile): An optional parameter that allows a user to upload an image for their profile picture. 
                If no image is uploaded, then the default avatar will be used instead. 
    
    :param name: str: Get the name of the user from the request body
    :param file: UploadFile: Upload a file to the server
    :param current_user: User: Get the current user
    :param db: AsyncSession: Get the database session
    :return: A dictionary with the user and detail keys
    """
    user_exist = await repository_users.get_user_username(name, db)
    
    if user_exist:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this name aready exists!")
     
    user = await repository_users.edit_my_profile(current_user.email, file, name, db)
    
    return {"user": user, "detail": "My profile was successfully edited"}


@router.get("/all_users",
            dependencies=[Depends(admin)],
            response_model=list[UserDb])
async def all_users(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(auth_service.get_current_user),
    redis_client: Redis = Depends(init_async_redis),
    db: AsyncSession = Depends(get_db)
) -> list:
    """
    The all_users function returns a list of all users in the database.
    
    :param skip: int: Skip a number of users in the database
    :param limit: int: Limit the number of users returned
    :param current_user: User: Get the current user
    :param redis_client: Redis: Pass in the redis client object
    :param db: AsyncSession: Create a database connection
    :return: A list of user objects
    """
    key_to_clear = f"user:{current_user.email}"
    await redis_client.delete(key_to_clear)
    
    users = await repository_users.get_all_users(skip, limit, db)
    return users  

@router.get("/{username}",
            dependencies=[Depends(admin_moderator)],
            response_model=UserProfile)
async def user_profile(
    username: str,
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    The user_profile function returns the user profile of a given username.
    
    :param username: str: Get the username of the user we want to update
    :param current_user: User: Get the user that is currently logged in
    :param db: AsyncSession: Get the database session
    :param : Get the current user
    :return: A user object
    """
    user_exist = await repository_users.get_user_username(username, db)
    if user_exist:
        user = await repository_users.get_user_profile(user_exist, db)
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found!")
    
    
@router.patch("/ban_user",
            dependencies=[Depends(admin_moderator)],
            response_model=UserResponse)
async def ban_user(
    username: str,
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    user_banned = await repository_users.get_user_username(username, db)
    if user_banned:
        if user_banned.username == current_user.username:
            return {"user":user_banned, "detail": "You can't ban yourself"}
        else:
            user = await repository_users.ban_user(user_banned.email, db)
            return {"user": user, "detail": f"The user {user_banned.username} has been banned"}
    else:
        raise HTTPException(status_code=404, detail="User not found!")


@router.patch("/activate_user",
            dependencies=[Depends(admin)],
            response_model=UserResponse)
async def activate_user(
    username: str,
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    user_activate = await repository_users.get_user_username(username, db)
    if user_activate:
        user = await repository_users.activate_user(user_activate.email, db)
        return {"user": user, "detail": f"The user {user_activate.username} has been activated"}
    else:
        raise HTTPException(status_code=404, detail="User not found!")