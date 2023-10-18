from typing import Any, Sequence

from sqlalchemy import select, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Comment
from src.schemas.comments import CommentCreate, CommentUpdate
from fastapi import HTTPException, status


async def create_comment(
    body: CommentCreate,
    picture_id,
    user_id,
    db: AsyncSession,
) -> Comment:
    """
    The create_comment function creates a new comment in the database.

    :param body: CommentCreate: Specify the type of data that is expected to be passed in
    :param db: AsyncSession: Pass in the database session
    :param : Get the comment id from the url
    :return: A comment object
    """

    new_comment = Comment(**body.model_dump(), picture_id=picture_id, user_id=user_id)
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    return new_comment


async def update_comment(comment_id: int, body: CommentUpdate, current_user: int, db: AsyncSession) -> Comment:
    """
    The update_comment function updates a comment in the database.
        It takes in an id of the comment to be updated, and a CommentUpdate object containing the new text for that comment.
        The function then checks if there is an existing user with that id, and if so it updates their text field with
        whatever was passed into CommentUpdate's text field. If no such user exists, it raises a 404 error.

    :param comment_id: int: Get the comment id
    :param body: CommentUpdate: Get the updated comment text from the request body
    :param current_user: int: Get the user_id of the current user
    :param db: AsyncSession: Pass the database session to the function
    :return: The updated comment
    """

    comment_query = select(Comment).where(Comment.id == comment_id, Comment.user_id == current_user)
    existing_comment = await db.execute(comment_query)
    comment = existing_comment.scalar()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment is not found")

    if body.text == "":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Comment can't be empty")

    comment.text = body.text
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


async def delete_comment(comment_id: int, db: AsyncSession) -> Comment:
    """
    The delete_comment function deletes a comment from the database.

    :param comment_id: int: Identify the comment to be deleted
    :param db: AsyncSession: Pass the database session to the function
    :return: None
    """

    comment_query = select(Comment).where(Comment.id == comment_id)
    existing_comment = await db.execute(comment_query)
    comment = existing_comment.scalar()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment is not found")
    try:
        await db.delete(comment)
        await db.commit()
        return comment
    except Exception as error:
        await db.rollback()
        raise error


async def get_comments_to_photo(skip: int, limit: int, picture_id: int, db: AsyncSession) -> Sequence[Row | RowMapping | Any]:
    """
    The get_comments_to_photo function returns a list of comments to the picture with id = picture_id.
    The function takes three arguments: skip, limit and picture_id.
    Skip is an integer that indicates how many comments should be skipped before returning the result.
    Limit is an integer that indicates how many comments should be returned in total (after skipping).
    Picture_id is an integer that represents the id of a particular photo.

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


async def get_comments_of_user(skip: int, limit: int, user_id: int, db: AsyncSession) -> Sequence[Row | RowMapping | Any]:
    """
    The get_comments_of_user function returns a list of comments made by the user with the given id.

    :param skip: int: Skip a certain number of rows
    :param limit: int: Limit the number of comments returned
    :param user_id: int: Filter the comments by user
    :param db: AsyncSession: Pass the database session to the function
    :return: A list of comments
    """

    query = select(Comment).where(Comment.user_id == user_id).offset(skip).limit(limit)
    comments = await db.execute(query)
    result = comments.scalars().all()
    return result
