from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from src.database.models import Tag
from src.schemas.tags_schema import TagModel, TagResponse

async def get_tags(db: AsyncSession):
    async with db.begin():
        query = await db.execute(select(Tag))
        tags = query.scalars().all()
        return tags
    
async def get_tag_by_id(tag_id: int, db: AsyncSession):
    async with db.begin():
        query = select(Tag).filter(Tag.id == tag_id) 
        tag = await db.execute(query)
        result = tag.scalar()
        return result
    
async def get_tag_by_tagname(tagname: str, db: AsyncSession):
    async with db.begin():
        query = select(Tag).filter(Tag.tagname == tagname) 
        tag = await db.execute(query)
        result = tag.scalar()
        return result

async def create_tag(body: TagModel, db: AsyncSession):
    async with db.begin():
        tag = Tag(**body.dict())
        db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return tag

async def update_tag(tag_id: int, body: TagModel, db: AsyncSession):
    tag = await get_tag_by_id(tag_id, db)
    
    if tag: 
        async with db.begin():
            tag.tagname = body.tagname
        
            tag_response = TagResponse(
                id=tag.id,
                tagname=tag.tagname,
                created_at=tag.created_at,
                updated_at=tag.updated_at
            )

        return tag_response
    

async def remove_tag(tag_id: int, db: AsyncSession):
    tag = await get_tag_by_id(tag_id, db)
    
    if tag:
        async with db.begin():
            await db.delete(tag)
            await db.commit()
    
