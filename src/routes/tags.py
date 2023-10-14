from typing import List

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository import tags as repository_tags
from src.database.db import get_db
from src.database.models import Tag
from src.schemas.tags_schema import TagResponse, TagModel

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get('', response_model=List[TagResponse])
async def get_tags(db: AsyncSession = Depends(get_db)):
    tags = await repository_tags.get_tags(db)
    return tags

@router.get('/{tag_id}', response_model=TagResponse)
async def get_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    tag = await repository_tags.get_tag_by_id(tag_id, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tagname not found")
    return tag

@router.post('', response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(body: TagModel, db: AsyncSession = Depends(get_db)):
    exist_tag = await repository_tags.get_tag_by_tagname(tagname=str(body.tagname), db=db)
    if exist_tag:
        # raise HTTPException(status_code=status.HTTP_201_CREATED, detail="tagname already exist!")
        return exist_tag
    tag = await repository_tags.create_tag(body, db)
    return tag

@router.patch("/{tag_id}", response_model=TagResponse)
async def update_tag(tag_id: int, body: TagModel, db: AsyncSession = Depends(get_db)):
    tag = await repository_tags.get_tag_by_id(tag_id, db)
    exist_tag = await repository_tags.get_tag_by_tagname(str(body.tagname), db)
    
    if tag:
        if exist_tag is None:
            updated_tag = await repository_tags.update_tag(tag_id, body, db)
            return updated_tag  
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="tagname already exist")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tagname not found")

@router.delete('/{tag_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    tag = await repository_tags.get_tag_by_id(tag_id, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tagname not found")
    
    result = await repository_tags.remove_tag(tag_id, db)
    return result
        
    