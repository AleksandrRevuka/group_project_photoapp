from datetime import datetime
import enum
from typing import List

from pydantic import BaseModel, ConfigDict, EmailStr

from src.database.models import Role
from src.schemas.comments import CommentDB
from src.schemas.pictures import PictureUser


class UserModel(BaseModel):
    """
    Represents a user model.

    Attributes:
        username (str): The username of the user.
        email (str): The email address of the user.
        password (str): The password of the user.
    """

    username: str
    email: str
    password: str


class UserDb(BaseModel):
    """
    Represents a user in the database.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        avatar (str): The avatar URL of the user.
        roles (Role): The roles associated with the user.

    Configured with:
        from_attributes (bool): Flag indicating if the attributes should be used for configuration.
    """

    id: int
    username: str
    email: str
    avatar: str
    roles: Role


class RatingDB(BaseModel):
    id: int
    rating: int
    picture_id: int


class UserInfo(UserDb):
    model_config = ConfigDict(from_attributes=True)

    email: str
    roles: Role
    created_at: datetime
    updated_at: datetime

    pictures: List[PictureUser]
    comments_user: List[CommentDB]
    ratings: List[RatingDB]


class UserResponse(BaseModel):
    """
    Represents a response containing user information.

    Attributes:
        user (UserDb): The user information.
        detail (str): Additional detail message (default: "User successfully created").
    """

    user: UserDb
    detail: str = "User"


class MessageResponse(BaseModel):
    """
    Represents a response containing a message.

    Attributes:
        message (str): The message (default: "This is a message").
    """

    message: str = "This is a message"


class TokenModel(BaseModel):
    """
    Represents a token model.

    Attributes:
        access_token (str): The access token.
        refresh_token (str): The refresh token.
        token_type (str): The token type (default: "bearer").
    """

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    """
    Represents a request containing an email.

    Attributes:
        email (EmailStr): The email address.
    """

    email: EmailStr


class ResetPassword(BaseModel):
    """
    Represents a reset password request.

    Attributes:
        new_password (str): The new password.
        confirm_password (str): The confirmation of the new password.
    """

    new_password: str
    confirm_password: str


class UserProfile(BaseModel):
    id: int
    username: str
    email: EmailStr
    confirmed: bool
    avatar: str
    roles: Role
    is_active: bool
    pictures_count: int | None
    comments_count: int | None
    created_at: datetime | None
    updated_at: datetime | None
    
        
class Action(enum.Enum):
    ban: str = "ban"
    activate: str = "activate"
    change_role: str = "change_role"
    
