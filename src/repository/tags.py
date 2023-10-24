from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from src.database.models import Picture, Tag
from src.schemas.tags import TagModel, TagResponse


async def get_tags(db: AsyncSession):
    """
    The get_tags function is a coroutine that returns all tags in the database.
    It takes an AsyncSession object as its only argument, and it uses this session to execute a query on the Tag table.
    The result of this query is returned as a list of strings.

    :param db: AsyncSession: Pass the database session to the function
    :return: A list of tags
    :doc-author: Trelent
    """
    query = await db.execute(select(Tag))
    tags = query.scalars().all()
    return tags


async def get_tag_by_id(tag_id: int, db: AsyncSession):
    """
    The get_tag_by_id function takes in a tag_id and an AsyncSession object.
    It then uses the AsyncSession to query the database for a Tag with that id.
    If it finds one, it returns that Tag as an object.

    :param tag_id: int: Specify the id of the tag we want to retrieve from our database
    :param db: AsyncSession: Pass the database session into the function
    :return: A tag object
    :doc-author: Trelent
    """
    query = select(Tag).filter(Tag.id == tag_id)
    tag = await db.execute(query)
    result = tag.scalar()
    return result


async def get_tag_by_tagname(tagname: str, db: AsyncSession):
    """
    The get_tag_by_tagname function takes in a tagname and an AsyncSession object.
    It then queries the database for a Tag with that tagname, and returns it as a
    TagModel object.

    :param tagname: str: Filter the query by tagname
    :param db: AsyncSession: Pass the database session to the function
    :return: A tag object that has the given tagname
    :doc-author: Trelent
    """
    query = select(Tag).filter(Tag.tagname == tagname)
    tag = await db.execute(query)
    result = tag.scalar()
    return result


async def update_tag(tag_id: int, body: TagModel, db: AsyncSession):
    """
    The update_tag function takes in a tag_id, body, and db.
        It then gets the tag by id from the database. If it exists,
        it updates the tagname to what is passed in through body.

    :param tag_id: int: Get the tag by id
    :param body: TagModel: Pass in the new tagname to update the tag with
    :param db: AsyncSession: Create a database connection to the postgres database
    :return: A tagresponse object
    :doc-author: Trelent
    """
    tag = await get_tag_by_id(tag_id, db)

    if tag:
        tag.tagname = body.tagname

        tag_response = TagResponse(id=tag.id, tagname=tag.tagname, created_at=tag.created_at, updated_at=tag.updated_at)

        return tag_response


async def remove_tag(tag_id: int, db: AsyncSession):
    """
    The remove_tag function removes a tag from the database.

    :param tag_id: int: Specify the id of the tag to be removed
    :param db: AsyncSession: Pass the database session to the function
    :return: The tag that was removed
    :doc-author: Trelent
    """
    tag = await get_tag_by_id(tag_id, db)

    if tag:
        await db.delete(tag)
        await db.commit()



