from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy import func, select

from src.database.models import User, Rating, Picture
from src.conf.messages import messages


async def create_picture_rating(
    picture_id: int,
    rating: int,
    current_user: User,
    db: AsyncSession,
) -> Rating:
    """
    Create a new rating for a picture.

    This function creates a new rating for the picture with the given ID. It ensures that the current user is not
    rating their own picture. If an existing rating is found, it will return an error message.

    :param picture_id: int: The ID of the picture in the database.
    :param rating: int: The rating value from the request body.
    :param current_user: User: The User object representing the current logged-in user.
    :param db: AsyncSession: The database session used for database queries.

    :return: Rating: The newly created rating object.
    """

    picture = await db.get(Picture, picture_id)
    if not picture or picture.user_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.get_message("YOU_CANT_RATE_YOUR_OWN_PICTURE"))

    exist_rating = await db.execute(select(Rating).where((Rating.user_id == current_user.id) & (Rating.picture_id == picture_id)))
    existing_rating = exist_rating.scalar()

    if existing_rating:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.get_message("YOU_HAVE_ALREADY_RATED_THIS_PICTURE"))

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
    Remove a rating from the database.

    This function removes a rating associated with a specific picture and user from the database.

    :param picture_id: int: The ID of the picture that was rated.
    :param user_id: int: The ID of the user who rated the picture.
    :param db: AsyncSession: The database session used for database operations.

    :return: Rating: The removed rating object.
    """
    query = await db.execute(select(Rating).where((Rating.user_id == user_id) & (Rating.picture_id == picture_id)))
    rating = query.scalar()
    if not rating:
        return None

    await db.delete(rating)
    await db.commit()
    return rating
