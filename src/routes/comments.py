from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas.comments import CommentCreate, CommentDB, CommentUpdate
from src.services.roles import admin_moderator_user, admin_moderator
from src.repository import comments as repository_comments
from src.services.auth import auth_service
from src.database.models import User
from src.conf.messages import messages


router = APIRouter(tags=["comments"])


@router.post(
    "/{picture_id}/comments",
    dependencies=[Depends(admin_moderator_user)],
    description="User, Moderator and Administrator have access",
)
async def create_comment(
    picture_id: int,
    body: CommentCreate,
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    The create_comment function creates a new comment in the database.

    :param body: CommentCreate: Create a new comment
    :param db: AsyncSession: Pass the database connection to the repository
    
    :return: A comment object
    """

    comment = await repository_comments.create_comment(body, picture_id, current_user.id, db)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.get_message("COMMENT_NOT_CREATED"))
    return comment


@router.patch(
    "/{picture_id}/comments/{comment_id}",
    dependencies=[Depends(admin_moderator_user)],
    description="User, Moderator and Administrator have access",
)
async def update_comment(
    comment_id: int,
    picture_id: int,
    body: CommentUpdate,
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    The update_comment function updates a comment in the database.
        The function takes an id of the comment to be updated, and a CommentUpdate object containing
        the new values for each field. It then checks if there is already a comment with that id, and if so it updates it with
        the new values from CommentUpdate. If not, it raises an HTTPException indicating that no such comment exists.

    :param comment_id: int: Identify the comment that is being updated
    :param body: CommentUpdate: Get the data from the request body
    :param current_user: User: Get the current user from the auth_service
    :param db: AsyncSession: Get the database session

    :return: A comment object
    """

    comment = await repository_comments.update_comment(picture_id, comment_id, body, current_user.id, db)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.get_message("COMMENT_NOT_CREATED"))
    return comment


@router.delete(
    "/{picture_id}/comments/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(admin_moderator)],
    description="Moderator and Administrator have access",
)
async def remove_comment(
    picture_id: int,
    comment_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    The delete_comment function deletes a comment from the database.
        Args:
            comment_id (int): The id of the comment to be deleted.
            db (AsyncSession): An async session object for interacting with the database.

    :param comment_id: int: Identify the comment to be deleted
    :param db: AsyncSession: Pass in the database session

    :return: A 204 status code
    """
    comment = await repository_comments.delete_comment(comment_id, picture_id, db)
    return comment


@router.get(
    "/{picture_id}/comments",
    response_model=List[CommentDB],
    dependencies=[Depends(admin_moderator_user)],
    description="User, Moderator and Administrator have access",
)
async def comments_to_picture(
    picture_id: int,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    """
    The comments_to_picture function returns a list of comments to the picture with the given picture_id.
    The skip and limit parameters are used for pagination, where skip is how many comments to skip and limit is how many
    comments to return.

    :param picture_id: int: Get the comments to a specific picture
    :param skip: int: Skip the first n comments
    :param limit: int: Limit the number of comments returned
    :param db: AsyncSession: Get the database session
    :return: A list of comments to a picture
    """

    comments = await repository_comments.get_comments_to_picture(skip, limit, picture_id, db)
    if not comments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.get_message("COMMENTS_NOT_FOUND"))
    return comments
