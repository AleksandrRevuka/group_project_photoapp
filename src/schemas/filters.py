from typing import List, Optional

from fastapi import Query
from fastapi_filter import FilterDepends, with_prefix
from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, ConfigDict, Field

from src.database.models import Comment, Picture, Role, Tag, User


class CommentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    text: str


class TagOut(BaseModel):
    id: int
    tagname: str


class PictureOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    rating_average: float
    tags_picture: Optional[List[TagOut]] = []
    comments_picture: Optional[List[CommentOut]] = []


class UserIn(BaseModel):
    username: str
    roles: Role

class PictureOut_(BaseModel):
    id: int
    name: str
    description: str
    rating_average: float


class UserOut(UserIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    pictures: Optional[List[PictureOut_]] = []
    comments_user: Optional[List[CommentOut]] = []


class CommentFilter(Filter):
    text__ilike: Optional[str] = None

    class Constants(Filter.Constants):
        model = Comment


class TagFilter(Filter):
    tagname__ilike: Optional[str] = None

    class Constants(Filter.Constants):
        model = Tag


class PictureFilter(Filter):
    id: Optional[int] = None
    name__ilike: Optional[str] = None
    description__ilike: Optional[str] = None
    rating_average: Optional[float] = None
    rating_average__lt: Optional[int] = None
    rating_average__gte: Optional[int] = None
    tags: Optional[TagFilter] = FilterDepends(with_prefix("tags", TagFilter))

    order_by: Optional[List[str]] = Field(
        Query(description="'id', 'name', 'description' or 'rating_average', '-'reverse", default="name")
    )

    class Constants(Filter.Constants):
        model = Picture


class UserFilter(Filter):
    id: Optional[int] = None
    username: Optional[str] = None
    username__ilike: Optional[str] = None
    username__like: Optional[str] = None
    comments: Optional[CommentFilter] = FilterDepends(with_prefix("comments", CommentFilter))
    order_by: Optional[List[str]] = Field(Query(description="'id' or 'username', '-'reverse", default="username"))

    class Constants(Filter.Constants):
        model = User
