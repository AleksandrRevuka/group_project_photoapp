from typing import List

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository import tags as repository_tags
from src.database.db import get_db
from src.schemas.tags import TagResponse, TagModel
from src.services.roles import admin_moderator
from src.conf.messages import messages

router = APIRouter(tags=["tags"])


@router.get(
    "/",
    response_model=List[TagResponse],
    dependencies=[Depends(admin_moderator)],
)
async def get_tags(db: AsyncSession = Depends(get_db)):
    """
    The get_tags function returns a list of all tags in the database.

    :param db: AsyncSession: Get a database connection from the dependency injection container
    
    :return: A list of all tags in the database
    """

    tags = await repository_tags.get_tags(db)
    return tags


@router.get("/{tag_id}", dependencies=[Depends(admin_moderator)], response_model=TagResponse)
async def get_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    """
    The get_tag function returns a tag object by its id.

    :param tag_id: int: Get the tag_id from the url
    :param db: AsyncSession: Get the database session from the dependency
    :return: A tag object, which is a dict
    """
    tag = await repository_tags.get_tag_by_id(tag_id, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.get_message("TAGNAME_NOT_FOUND"))
    return tag


@router.patch("/{tag_id}", dependencies=[Depends(admin_moderator)], response_model=TagResponse)
async def update_tag(tag_id: int, body: TagModel, db: AsyncSession = Depends(get_db)):
    """
    The update_tag function updates a tag in the database.
        It takes an id and a body as parameters, and returns the updated tag.


    :param tag_id: int: Get the tag_id from the url
    :param body: TagModel: Get the tagname from the request body
    :param db: AsyncSession: Get the database session
    :return: The updated tag, if the tagname does not exist it will return an error
    :doc-author: Trelent
    """
    tag = await repository_tags.get_tag_by_id(tag_id, db)
    exist_tag = await repository_tags.get_tag_by_tagname(str(body.tagname), db)

    if tag:
        if exist_tag is None:
            updated_tag = await repository_tags.update_tag(tag_id, body, db)
            return updated_tag
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=messages.get_message("TAGNAME_ALREADY_EXIST"))
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.get_message("TAGNAME_NOT_FOUND"))


@router.delete("/{tag_id}", dependencies=[Depends(admin_moderator)], status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    """
    The delete_tag function deletes a tag from the database.
        It takes in an integer, tag_id, and returns a boolean value indicating whether or not the deletion was successful.

    :param tag_id: int: Get the tag id from the url
    :param db: AsyncSession: Get the database session
    :return: A boolean value
    :doc-author: Trelent
    """
    tag = await repository_tags.get_tag_by_id(tag_id, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.get_message("TAGNAME_NOT_FOUND"))

    result = await repository_tags.remove_tag(tag_id, db)
    return result
