
import cloudinary.uploader
from libgravatar import Gravatar
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from fastapi import UploadFile

from src.database.models import User
from src.schemas.user import UserModel
from src.conf.config import init_cloudinary


async def get_user_by_email(email: str, db: AsyncSession) -> User | None:
    """
    The get_user_by_email function takes in an email address and a database session.
    It then queries the database for a user with that email address, returning the first result if it exists.

    :param email: str: Specify the type of the email parameter
    :param db: AsyncSession: Pass the database session to the function
    :return: A user object if the user exists in the database
    """
    query = select(User).filter_by(email=email)
    result = await db.execute(query)
    user = result.scalars().first()
    return user


async def create_user(body: UserModel, db: AsyncSession) -> User:
    """
    The create_user function takes a UserModel object and a database session as arguments.
    It then creates an instance of the Gravatar class, passing in the user's email address.
    The get_image() method is called on this instance to retrieve the user's avatar image from Gravatar.com,
    and it is assigned to the avatar variable. The model_dump() method of UserModel returns a dictionary containing all
    the fields that are required for creating an instance of User (except for id). This dictionary is unpacked into
    keyword arguments for creating new_user using Python's ** operator.

    :param body: UserModel: Create a new user
    :param db: AsyncSession: Pass the database session to the function
    :return: A user object
    """
    g = Gravatar(body.email)
    avatar = g.get_image()
    new_user = User(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, refresh_token: str | None, db: AsyncSession) -> None:
    """
    The update_token function updates the refresh token for a user.

    :param user: User: Pass the user object to the function
    :param refresh_token: str: Update the refresh token in the database
    :param db: AsyncSession: Access the database
    :return: The updated user
    """
    if refresh_token:
        user.refresh_token = refresh_token
        await db.commit()


async def confirmed_email(email: str, db: AsyncSession) -> None:
    """
    The confirmed_email function takes an email address and a database session as arguments.
    It then queries the database for a user with that email address, and sets their confirmed field to True.
    Finally, it commits the change to the database.

    :param email: str: Specify the email address of the user to be confirmed
    :param db: AsyncSession: Pass in the database session
    :return: None
    """
    user = await get_user_by_email(email, db)
    if user:
        user.confirmed = True
        await db.commit()


async def edit_my_profile(email: str, file: UploadFile, name: str, db: AsyncSession) -> User | None:
    user = await get_user_by_email(email, db)
    if user:
        if name:
            user.username = name
        init_cloudinary()
        r = cloudinary.uploader.upload(file.file, public_id=f"avatar/{user.username}", overwrite=True)
        src_url = cloudinary.CloudinaryImage(f"avatar/{user.username}").build_url(
                width=250, height=250, crop="fill", version=r.get("version")
            )
        user.avatar = src_url
        try:
            await db.commit()
            await db.refresh(user)
            return user
        except Exception as e:
            await db.rollback()
            raise e
    return None


async def change_password(user: User, password: str, db: AsyncSession) -> User:
    """
    The change_password function takes in a user, body, and db.
    The function then sets the password of the user to be equal to the confirm_password field of body.
    It then adds this new information into our database and commits it.
    Finally, we refresh our database with this new information.

    :param user: User: Get the user object from the database
    :param body: ResetPassword: Get the new password from the request body
    :param db: AsyncSession: Access the database
    :return: The user object with the new password
    """
    user.password = password
    try:
        await db.commit()
        return user
    except Exception as e:
        await db.rollback()
        raise e


async def get_user_username(username: str, db: AsyncSession) -> User | None:
    """
    The get_user_username function takes in a username and an AsyncSession object.
    It then queries the database for a user with that username, returning the User object if it exists, or None otherwise.
    
    :param username: str: Specify the username of the user we want to retrieve
    :param db: AsyncSession: Pass the database session into the function
    :return: The user object if the username exists in the database, else none
    """
    
    try:
        result = await db.execute(select(User).filter(User.username == username))
        user = result.scalar_one_or_none()
        return user
    except NoResultFound:
        return None
