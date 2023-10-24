from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi_filter import FilterDepends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.conf.config import init_async_redis
from src.database.db import get_db
from src.database.models import Role, User
from src.repository import users as repository_users
from src.schemas.comments import CommentDB
from src.schemas.filters import UserFilter, UserOut
from src.schemas.users import Action, UserDb, UserInfo, UserProfile, UserResponse
from src.services.auth import auth_service
from src.services.roles import admin, admin_moderator, admin_moderator_user
from src.conf.messages import messages

router = APIRouter(tags=["users"])


@router.get("/me", response_model=UserInfo)
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


@router.patch("/me", response_model=UserResponse)
async def edit_my_profile(
    name: str,
    file: UploadFile = File(default=None),
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    The edit_my_profile function allows a user to edit their profile.

    :param name: str: Get the name of the user
    :param file: UploadFile: Upload a file to the server
    :param current_user: User: Get the current user
    :param db: AsyncSession: Get the database session

    :return: A dictionary with the user and a message
    """
    
    user_exist = await repository_users.get_user_username(name, db)

    if user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.get_message("USER_WITH_THIS_NAME_ALREADY_EXISTS"))

    user = await repository_users.edit_my_profile(current_user.email, file, name, db)

    return {"user": user, "detail": messages.get_message("MY_PROFILE_WAS_SUCCESSFULLY_EDITED")}


@router.get("/", dependencies=[Depends(admin_moderator_user)], response_model=List[UserOut])
async def search_users(
    user_filter: UserFilter = FilterDepends(UserFilter), 
    db: AsyncSession = Depends(get_db)):
    """
    The search_users function searches for users in the database.

    :param user_filter: UserFilter: Define the filter object that will be used to search for users
    :param db: AsyncSession: Get the database session
    :return: A list of users
    """

    users = await repository_users.search_users(user_filter, db)

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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.get_message("USER_NOT_FOUND"))


@router.patch("/{username}", dependencies=[Depends(admin_moderator)], response_model=UserResponse)
async def manage_user(
    username: str,
    action: Action,
    role: Role = Role.user,
    current_user: User = Depends(auth_service.get_current_user),
    redis_client: Redis = Depends(init_async_redis),
    db: AsyncSession = Depends(get_db),
):
    """
    Manage a user's status, role, or ban.
    
    This function allows administrators and moderators to perform actions on a user. Available actions are:
    - 'ban': Bans an active user. Raises an error if the user is already banned.
    - 'activate': Activates a banned user. Raises an error if the user is already active.
    - 'change_role': Changes the role of a user (except for admins) to a different role, excluding 'admin'.

    :param username: str: The username of the user to be managed.
    :param action: Action: The action to be taken on the user.
    :param role: Role: The new role for the user (optional, defaults to 'user').
    :param current_user: User: The current user performing the action.
    :param redis_client: Redis: The Redis client used for caching (dependency).
    :param db: AsyncSession: The database session (dependency).

    :return: Tuple[User, str]: A tuple containing the updated user and a message detailing the action.
    """

    user_action = await repository_users.get_user_username(username, db)

    if not user_action:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.get_message("USER_NOT_FOUND"))

    key_to_clear = f"user:{user_action.email}"
    await redis_client.delete(key_to_clear)

    if user_action.username == current_user.username:
            return {"user": user_action, "detail": messages.get_message("YOU_CANT_BAN_YOURSELF")}
  
    if action == Action.ban:
        if current_user.roles == (Role.admin or Role.moderator):
            if user_action.is_active:
                if user_action.username == current_user.username:
                    return {"user": user_action, "detail": messages.get_message("YOU_CANT_BAN_YOURSELF")}
                else:
                    user = await repository_users.ban_user(user_action.email, db)
                    return {"user": user, "detail": f"{user_action.username} " + messages.get_message("USER_HAS_BEEN_BANNED")}
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.get_message("USER_HAS_ALREADY_BANNED"))
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.get_message("YOU_DONT_HAVE_PERMISSION_TO_BAN_USERS"))

    elif action == Action.activate:
        if current_user.roles == Role.admin:
            if not user_action.is_active:
                user = await repository_users.activate_user(user_action.email, db)
                return {"user": user, "detail": f"{user_action.username} " + messages.get_message("USER_HAS_BEEN_ACTIVATED")}
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.get_message("USER_ALREADY_ACTIVATED"))
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.get_message("YOU_DONT_HAVE_PERMISSION_FOR_ACTIVATE_USERS"))

    elif action == Action.change_role:
        if current_user.roles == Role.admin:
            if role is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                    detail=messages.get_message("NEW_ROLE_MUST_BE_SPECIFIED_FOR_CHANGING_ROLE"))
            
            user = await repository_users.change_role(user_action.email, role, db)
            return {"user": user, "detail": messages.get_message("USERS_ROLE_HAS_BEEN_CHANGED_TO") + f" {role}"}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail=messages.get_message("YOU_DONT_HAVE_PERMISSION_FOR_CHANGE_USER_ROLES"))
    
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail=messages.get_message("INVALID_ACTION_SPECIFIED"))