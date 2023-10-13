import enum
from datetime import date, datetime
from typing import List

from sqlalchemy import Date, DateTime, Enum, String, func, Table, Integer, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey


class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy models.
    """

class BaseWithTimestamps(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

class Role(enum.Enum):
    """
    Enum representing user roles.

    Attributes:
        admin (str): Admin role.
        moderator (str): Moderator role.
        user (str): User role.
    """

    admin: str = "admin"
    moderator: str = "moderator"
    user: str = "user"


class User(Base, BaseWithTimestamps):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    confirmed: Mapped[bool] = mapped_column(default=False)

    password: Mapped[str] = mapped_column(String(255), nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    roles: Mapped[Enum] = mapped_column("roles", Enum(Role), default=Role.user)

picture_tags = Table(
    'picture_tags', 
    Base.metadata,
    Column('picture_id', Integer, ForeignKey('pictures.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Tag(Base, BaseWithTimestamps):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(primary_key=True)
    tagname: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

class Comment(Base, BaseWithTimestamps):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String(200), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    picture_id: Mapped[int] = mapped_column(ForeignKey("pictures.id"))

class Picture(Base, BaseWithTimestamps):
    __tablename__ = "pictures"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    picture_url: Mapped[str] = mapped_column(String(200), nullable=False)
    create_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    tags: Mapped[List["Tag"]] = relationship("Tag", secondary=picture_tags, backref="pictures")