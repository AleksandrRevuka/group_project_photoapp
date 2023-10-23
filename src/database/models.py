import enum
from datetime import datetime, timedelta
from typing import List

from sqlalchemy import (Boolean, Column, DateTime, Enum, Float, Integer,
                        String, Table, event, func)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey

from src.conf.constant import REFRESH_TOKEN_TTL


class Base(AsyncAttrs, DeclarativeBase):
    """
    Base class for SQLAlchemy models.

    """
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


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


picture_tags = Table(
    "picture_tags",
    Base.metadata,
    Column("picture_id", Integer, ForeignKey("pictures.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
)


class User(Base, BaseWithTimestamps):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    roles: Mapped[Role] = mapped_column("roles", Enum(Role), default=Role.user)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    pictures: Mapped[list["Picture"]] = relationship("Picture", back_populates="user", cascade="all, delete")
    comments_user: Mapped[list["Comment"]] = relationship("Comment", back_populates="user", cascade="all, delete")
    ratings: Mapped[list["Rating"]] = relationship("Rating", back_populates="user")


class Tag(Base, BaseWithTimestamps):
    __tablename__ = "tags"

    tagname: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    pictures_teg: Mapped[List["Picture"]] = relationship(
        "Picture",
        secondary=picture_tags,
        back_populates="tags_picture",
        passive_deletes=True,
    )


class Comment(Base, BaseWithTimestamps):
    __tablename__ = "comments"

    text: Mapped[str] = mapped_column(String(200), nullable=False)
    picture_id: Mapped[int] = mapped_column(Integer, ForeignKey("pictures.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    picture: Mapped["Picture"] = relationship("Picture", back_populates="comments_picture", lazy="joined")
    user: Mapped[int] = relationship("User", back_populates="comments_user", lazy="joined")


class Picture(Base, BaseWithTimestamps):
    __tablename__ = "pictures"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    picture_url: Mapped[str] = mapped_column(String(200), nullable=False)
    rating_average: Mapped[float] = mapped_column(Float, default=0.0)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="pictures", lazy="joined")
    comments_picture: Mapped[list["Comment"]] = relationship("Comment", back_populates="picture", cascade="all, delete-orphan")
    tags_picture: Mapped[List["Tag"]] = relationship("Tag", secondary=picture_tags, back_populates="pictures_teg")
    ratings: Mapped["Rating"] = relationship("Rating", back_populates="picture", cascade="all, delete-orphan")


class Rating(Base, BaseWithTimestamps):
    __tablename__ = "ratings"

    rating: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    picture_id: Mapped[int] = mapped_column(Integer, ForeignKey("pictures.id"))

    user: Mapped["User"] = relationship("User", back_populates="ratings", lazy="joined")
    picture: Mapped[int] = relationship("Picture", back_populates="ratings", lazy="joined")


class InvalidToken(Base, BaseWithTimestamps):
    __tablename__ = "invalid_tokens"

    token: Mapped[str] = mapped_column(String(250), nullable=False)


@event.listens_for(InvalidToken, "after_insert")
def check_and_delete_old_tokens(mapper, connection, target):
    seven_days_ago = datetime.utcnow() - timedelta(seconds=REFRESH_TOKEN_TTL)

    connection.execute(InvalidToken.__table__.delete().where(InvalidToken.created_at < seven_days_ago))
