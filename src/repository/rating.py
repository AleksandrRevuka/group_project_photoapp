from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy import func, select

from src.database.models import User, Rating, Picture


async def create_picture_rating(
    picture_id: int,
    rating: int,
    current_user: User,
    db: AsyncSession,
) -> Rating:
    """
    The create_picture_rating function creates a new rating for the picture with the given id.
        The current_user is used to ensure that they are not rating their own picture, and also to ensure
        that they have not already rated this picture.
        If there is an existing rating, then it will be updated instead of creating a new one.

    :param picture_id: int: Get the picture that is being rated
    :param rating: int: Set the rating of the picture
    :param current_user: User: Get the id of the user who is currently logged in
    :param db: AsyncSession: Pass the database session to the function
    :param : Get the picture id
    :return: A rating object
    """

    picture = await db.get(Picture, picture_id)
    if not picture or picture.user_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot rate your own picture")

    exist_rating = await db.execute(select(Rating).where((Rating.user_id == current_user.id) & (Rating.picture_id == picture_id)))
    existing_rating = exist_rating.scalar()

    if existing_rating:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already rated this picture")

    new_rating = Rating(user_id=current_user.id, picture_id=picture_id, rating=rating)
    db.add(new_rating)
    await db.commit()
    await db.refresh(new_rating)

    average_rating = await calculate_average_rating(picture_id, db)
    if average_rating:
        picture.rating_average = average_rating
        await db.commit()

    return new_rating


async def calculate_average_rating(picture_id: int, db: AsyncSession) -> float | None:
    """
    The calculate_average_rating function calculates the average rating of a picture.

    :param picture_id: int: Specify the picture_id of the picture we want to calculate
    :param db: AsyncSession: Pass in the database session
    :return: A float or none
    """
    query = select(func.avg(Rating.rating).label("average_rating")).where(Rating.picture_id == picture_id)
    result = await db.execute(query)
    rating = result.scalar()
    return rating


async def picture_ratings(picture_id: int, db: AsyncSession):
    """
    The picture_ratings function takes in a picture_id and returns the ratings for that picture.
        Args:
            picture_id (int): The id of the desired picture.

    :param picture_id: int: Specify the picture id of the picture that is being rated
    :param db: AsyncSession: Pass the database connection to the function
    :return: A picture object
    """
    query = select(Picture).where(Picture.id == picture_id)
    result = await db.execute(query)
    picture = result.scalar_one_or_none()
    return picture


async def remove_rating(
    picture_id: int,
    user_id: int,
    db: AsyncSession,
):
    """
    The remove_rating function removes a rating from the database.

    :param picture_id: int: Find the picture that is being rated
    :param user_id: int: Specify the user who is rating the picture
    :param db: AsyncSession: Pass the database session to the function
    :param : Specify the picture id
    :return: The removed rating
    """
    query = await db.execute(select(Rating).where((Rating.user_id == user_id) & (Rating.picture_id == picture_id)))
    rating = query.scalar()
    if not rating:
        return None

    await db.delete(rating)
    await db.commit()
    return rating
