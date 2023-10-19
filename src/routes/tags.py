from typing import List

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository import tags as repository_tags
from src.database.db import get_db
from src.schemas.tags_schema import TagResponse, TagModel
from src.services.roles import admin_moderator

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get(
    "",
    response_model=List[TagResponse],
    dependencies=[Depends(admin_moderator)],
)
async def get_tags(db: AsyncSession = Depends(get_db)):
    """
    The get_tags function returns a list of all tags in the database.
        ---
        get:
            description: Get a list of all tags in the database.
            responses:  # A dictionary containing status codes and their corresponding responses. The keys are HTTP
            status codes, and the values are dictionaries with two keys, "description" (a string) and "content"
            (a dictionary). The content key's value is another dictionary that contains one key-value
            pair for each media type supported by this endpoint; for example, {"application/json": {...}}
            would be used to describe JSON output.

    :param db: AsyncSession: Pass in the database session
    :return: A list of tags
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tagname not found")
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
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="tagname already exist")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tagname not found")


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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tagname not found")

    result = await repository_tags.remove_tag(tag_id, db)
    return result


@router.get(
    "/picture/{picture_id}",
    response_model=List[TagResponse],
    dependencies=[Depends(admin_moderator)],
    description="User, Moderator and Administrator have access",
)
async def tags_of_picture(
    picture_id: int,
    db: AsyncSession = Depends(get_db),
) -> list:
    """
    The tags_of_picture function retrieves all tags for a given picture.
        Args:
            picture_id (int): The id of the picture to retrieve tags for.

    :param picture_id: int: Specify the picture id of the picture we want to retrieve
    :param db: AsyncSession: Pass the database session to the function
    :param : Get the picture id from the url
    :return: A list of tags for a given picture
    """
    tags = await repository_tags.retrieve_tags_for_picture(picture_id, db)
    return tags
