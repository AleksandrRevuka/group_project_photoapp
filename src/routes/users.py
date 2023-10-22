from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.conf.config import init_async_redis
from src.database.db import get_db
from src.database.models import Role, User
from src.repository import users as repository_users
from src.schemas.users import UserDb, UserInfo, UserProfile, UserResponse
from src.services.auth import auth_service
from src.services.roles import admin, admin_moderator

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/", response_model=UserInfo)
async def read_users_me(
    current_user: User = Depends(auth_service.get_current_user), redis_client: Redis = Depends(init_async_redis)
) -> User:
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
    file: UploadFile = File(default=None),
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this name already exists!")

    user = await repository_users.edit_my_profile(current_user.email, file, name, db)

    return {"user": user, "detail": "My profile was successfully edited"}


@router.get("/all_users", dependencies=[Depends(admin)], response_model=list[UserDb])
async def all_users(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(auth_service.get_current_user),
    redis_client: Redis = Depends(init_async_redis),
    db: AsyncSession = Depends(get_db),
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


@router.get("/{username}", dependencies=[Depends(admin_moderator)], response_model=UserProfile)
async def user_profile(
    username: str,
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    The user_profile function returns a user's profile information.

    :param username: str: Get the username from the request
    :param db: AsyncSession: Inject the database session into the function
    :return: A user object

    """

    user_exist = await repository_users.get_user_username(username, db)
    if user_exist:
        user = await repository_users.get_user_profile(user_exist, db)
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")


@router.patch("/ban_user", dependencies=[Depends(admin_moderator)], response_model=UserResponse)
async def ban_user(
    username: str,
    current_user: User = Depends(auth_service.get_current_user),
    redis_client: Redis = Depends(init_async_redis),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    The ban_user function is used to ban a user.

    :param username: str: Get the username of the user that will be banned
    :param current_user: User: Get the current user logged in
    :param redis_client: Redis: Connect to the redis database
    :param db: AsyncSession: Get the database session
    :return: A dictionary with the user and a detail message
    """

    user_banned = await repository_users.get_user_username(username, db)

    if user_banned:
        key_to_clear = f"user:{user_banned.email}"
        await redis_client.delete(key_to_clear)

        if user_banned.username == current_user.username:
            return {"user": user_banned, "detail": "You can't ban yourself"}
        elif not user_banned.is_active:
            return {"user": user_banned, "detail": "User has already been banned"}

        else:
            user = await repository_users.ban_user(user_banned.email, db)
            return {"user": user, "detail": f"The user {user_banned.username} has been banned"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")


@router.patch("/activate_user", dependencies=[Depends(admin)], response_model=UserResponse)
async def activate_user(
    username: str,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    The activate_user function is used to activate a user.
        The function takes in the username of the user to be activated and returns a dictionary containing
        the details of that user and an appropriate message.

    :param username: str: Get the username of the user to be deactivated
    :param db: AsyncSession: Get the database connection
    :return: The user and a detail message
    """
    user_activate = await repository_users.get_user_username(username, db)
    if user_activate:
        user = await repository_users.activate_user(user_activate.email, db)
        return {"user": user, "detail": f"The user {user_activate.username} has been activated"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")


@router.patch("/change_role", dependencies=[Depends(admin)], response_model=UserResponse)
async def change_role(
    username: str,
    role: Role,
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    The change_role function allows the admin to change the role of a user.
        The function takes in three parameters: username, role and current_user.
        The username parameter is used to get the user from the database using
        repository_users.get_user_username(). If this returns a valid user, then
        we check if that user is active and confirmed (not banned). If they are not
        banned or not confirmed, then we check if it's not our own account by comparing
        usernames with current_user.username != user.username . If all these conditions are met

    :param username: str: Get the username of the user whose role we want to change
    :param role: Role: Pass the role that will be assigned to the user
    :param current_user: User: Get the current user
    :param db: AsyncSession: Get the database session
    :return: A dictionary containing the user and a detail message
    """

    user = await repository_users.get_user_username(username, db)
    if user:
        if user.is_active and user.confirmed:
            if current_user.username != user.username:
                user = await repository_users.change_role(user.email, role, db)
                return {"user": user, "detail": "The user's role has been changed"}

            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can't change your role")
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="You can't change the role of a banned user or not confirmed"
            )
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
