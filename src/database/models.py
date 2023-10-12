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
    pass


class Role(enum.Enum):

    admin: str = "admin"
    moderator: str = "moderator"
    user: str = "user"



class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    confirmed: Mapped[bool] = mapped_column(default=False)

    password: Mapped[str] = mapped_column(String(255), nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    roles: Mapped[Enum] = mapped_column("roles", Enum(Role), default=Role.user)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())



picture_tags = Table(
    'picture_tags', 
    Base.metadata,
    Column('picture_id', Integer, ForeignKey('pictures.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

picture_comments = Table(
    "picture_comments",
    Base.metadata,
    Column('picture_id', Integer, ForeignKey("pictures.id")),
    Column("user_id", Integer, ForeignKey("users.id"))
)

class Tag(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(primary_key=True)
    tagname: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

class Comment(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String(200), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[relationship("User", back_populates="comments")] = relationship("User", back_populates="comments")
    picture_id: Mapped[int] = mapped_column(ForeignKey("pictures.id"))
    picture: Mapped[relationship("Picture", back_populates="comments")] = relationship("Picture", back_populates="comments")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

class Picture(Base):
    __tablename__ = "pictures"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    picture_url: Mapped[str] = mapped_column(String(200), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[relationship("User", back_populates="pictures")] = relationship("User", back_populates="pictures")
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    tags = Mapped[relationship("Tag", secondary=picture_tags, backref="pictures")]
    comments = Mapped[relationship("Comment", secondary=picture_comments, backref="pictures")]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

