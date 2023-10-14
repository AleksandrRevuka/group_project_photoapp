from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas.comments import CommentCreate, CommentUpdate
from src.database.models import Role, Picture, User
from src.services.roles import RoleAccess
from src.repository import comments as repository_comments


allowed_operation_get = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_create = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_update = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_remove = RoleAccess([Role.admin, Role.moderator])

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(allowed_operation_get)],
    description="User, Moderator and Administrator have access",
)
async def create_comment(
    body: CommentCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    The create_comment function creates a new comment in the database.

    :param body: CommentCreate: Create a new comment
    :param db: AsyncSession: Pass the database connection to the repository
    :param : Get the comment id from the url
    :return: A comment object
    """

    comment = await repository_comments.create_comment(body, db)
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not created"
        )
    return comment


@router.put(
    "/{body.comment_id}",
    dependencies=[Depends(allowed_operation_get)],
    description="User, Moderator and Administrator have access",
)
async def update_comment(
    body: CommentUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    The update_comment function updates a comment in the database.

    :param body: CommentUpdate: Pass the data from the request body to the function
    :param db: AsyncSession: Pass the database session to the repository
    :param : Get the comment id
    :return: A comment object
    """

    comment = await repository_comments.update_comment(body, db)
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not created"
        )
    return comment


@router.delete(
    "/{comment_id}",
    dependencies=[Depends(allowed_operation_remove)],
    description="Moderator and Administrator have access",
)
async def delete_comment(
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
    :param : Specify the id of the comment to be deleted
    :return: A 204 status code
    """
    comment = await repository_comments.delete_comment(comment_id, db)


@router.get(
    "/{picture_id}",
    dependencies=[Depends(allowed_operation_get)],
    description="User, moderator and admin",
)
async def get_comments_to_foto(
    skip: int = 0,
    limit: int = 10,
    picture_id: int = Picture.id,
    db: AsyncSession = Depends(get_db),
):
    """
    The get_comments_to_foto function returns a list of comments to the foto.
        ---
        get:
          summary: Get comments to foto.
          description: Returns a list of comments to the foto.  The number of items returned can be limited by using the limit parameter, and you can specify which page you want by using skip parameter (default is 0). You must also specify picture_id in order for this function to work properly.  If no results are found, an HTTP 404 error will be raised with detail &quot;Comments not found&quot;.

    :param skip: int: Skip the first n comments
    :param limit: int: Limit the number of comments returned
    :param picture_id: int: Get the comments to a specific picture
    :param db: AsyncSession: Pass the database session to the function
    :param : Get the id of a specific comment
    :return: A list of comments to the photo
    """

    comments = await repository_comments.get_comments_to_foto(
        skip, limit, picture_id, db
    )
    if not comments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comments not found"
        )
    return comments


@router.get(
    "/{user_id}",
    dependencies=[Depends(allowed_operation_get)],
    description="User, moderator and admin",
)
async def get_comments_of_user(
    skip: int = 0,
    limit: int = 10,
    user_id: int = User.id,
    db: AsyncSession = Depends(get_db),
):
    """
    The get_comments_of_user function returns a list of comments for the user with the given id.
    The function takes in an optional skip and limit parameter to paginate through results.

    :param skip: int: Skip the first n comments
    :param limit: int: Limit the number of comments returned
    :param user_id: int: Get the comments of a specific user
    :param db: AsyncSession: Get the database session
    :param : Get the comments of a specific user
    :return: A list of comments
    :doc-author: Trelent
    """

    comments = await repository_comments.get_comments_of_user(skip, limit, user_id, db)
    if not comments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comments not found"
        )
    return comments
