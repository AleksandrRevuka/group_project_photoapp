from typing import Sequence
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Comment, Picture
from src.schemas.comments import CommentCreate, CommentUpdate
from fastapi import HTTPException, status
from src.conf.messages import messages

async def create_comment(
    body: CommentCreate,
    picture_id,
    user_id,
    db: AsyncSession,
) -> Comment:
    """
    The create_comment function creates a new comment in the database.

    :param body: CommentCreate: Validate the data sent to the api
    :param picture_id: Get the picture id from the database
    :param user_id: Identify the user who created the comment
    :param db: AsyncSession: Pass the database session to the function
    
    :return: The newly created comment
    """

    new_comment = Comment(**body.model_dump(), picture_id=picture_id, user_id=user_id)
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    return new_comment


async def update_comment(picture_id: int, comment_id: int, body: CommentUpdate, current_user: int, db: AsyncSession) -> Comment:
    """
    Update a comment in the database.

    This function updates a comment in the database with the provided comment_id and new text from the CommentUpdate object.
    It checks if the current user is authorized to update the comment by comparing the user_id.

    :param picture_id: int: The ID of the picture associated with the comment.
    :param comment_id: int: The ID of the comment to update.
    :param body: CommentUpdate: The updated comment text from the request body.
    :param current_user: int: The user_id of the current user.
    :param db: AsyncSession: The database session.

    :return: Comment: The updated comment object.
    """

    comment_query = select(Comment).join(Picture).where(Comment.id == comment_id, Picture.id == picture_id, Comment.user_id == current_user)
    existing_comment = await db.execute(comment_query)
    comment = existing_comment.scalar()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.get_message("COMMENT_NOT_FOUND"))

    if body.text == "":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=messages.get_message("COMMENT_CANT_BE_EMPTY"))

    comment.text = body.text
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


async def delete_comment(comment_id: int, picture_id: int, db: AsyncSession) -> Comment:
    """
    The delete_comment function deletes a comment from the database.

    :param comment_id: int: Identify the comment to be deleted
    :param db: AsyncSession: Pass the database session to the function
    :return: None
    """

    comment_query = select(Comment).join(Picture).filter(Comment.id == comment_id, Picture.id == picture_id)
    existing_comment = await db.execute(comment_query)
    comment = existing_comment.scalar()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.get_message("COMMENT_NOT_FOUND"))
    try:
        await db.delete(comment)
        await db.commit()
        return comment
    except Exception as error:
        await db.rollback()
        raise error


async def get_comments_to_picture(skip: int, limit: int, picture_id: int, db: AsyncSession) -> Sequence[Comment]:
    """
    The get_comments_to_picture function returns a list of comments to the picture with id = picture_id.
    The function takes three arguments: skip, limit and picture_id.
    Skip is an integer that indicates how many comments should be skipped before returning the result.
    Limit is an integer that indicates how many comments should be returned in total (after skipping).
    Picture_id is an integer that represents the id of a particular picture.

    :param skip: int: Skip the first n comments
    :param limit: int: Limit the number of comments returned
    :param picture_id: int: Get comments to a specific picture
    :param db: AsyncSession: Pass the database session to the function
    :return: A list of comments
    """

    query = select(Comment).where(Comment.picture_id == picture_id).offset(skip).limit(limit)
    comments = await db.execute(query)
    result = comments.scalars().all()
    return result
