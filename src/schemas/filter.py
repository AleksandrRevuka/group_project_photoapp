from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from fastapi_filter import FilterDepends, with_prefix
from fastapi_filter.contrib.sqlalchemy import Filter
from fastapi import Query
from pydantic import Field

from src.database.models import Role, User, Picture, Comment, User

class CommentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    text:str

class PictureOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str
    rating_average: float

class UserIn(BaseModel):
    username: str
    roles: Role
    
        
class UserOut(UserIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    pictures: Optional[List[PictureOut]]
    comments_user: Optional[List[CommentOut]]
        
        
class CommentFilter(Filter):
    text__ilike: Optional[str] = None

    class Constants(Filter.Constants):
        model = Comment
        
class PictureFilter(Filter):
    name__ilike: Optional[str] = None
    description__ilike: Optional[str] = None
    rating_average: Optional[float] = None
    rating__lt: Optional[int] = None
    rating__gte: Optional[int] = None
    
    custom_order_by: Optional[List[str]] = None
    custom_search: Optional[str] = None
    
    class Constants(Filter.Constants):
        model = Picture
        ordering_field_name = "custom_order_by"
        search_field_name = "custom_search"
        search_model_fields = ["name", "description", "rating_average"]
     
        
class UserFilter(Filter):
    username: Optional[str] = None
    username__ilike: Optional[str] = None
    username__like: Optional[str] = None
    # pictures: Optional[PictureFilter] = FilterDepends(with_prefix("pictures", PictureFilter))
    # comments: Optional[CommentFilter] = FilterDepends(with_prefix("comments", CommentFilter))
    order_by: Optional[List[str]] = None
    
    class Constants(Filter.Constants):
        model = User
        search_model_fields = ["username"]