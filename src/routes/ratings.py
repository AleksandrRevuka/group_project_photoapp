from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


from src.database.db import get_db
from src.database.models import User
from src.repository import ratings as repository_rating
from src.schemas.ratings import RatingResponse, AverageRatingResponse
from src.services.auth import auth_service
from src.services.roles import admin, admin_moderator_user
from src.conf.messages import messages

router = APIRouter(tags=["rating"])


@router.post("{picture_id}/ratings", dependencies=[Depends(admin_moderator_user)], response_model=RatingResponse)
async def create_picture_rating(
    picture_id: int, rating: int, current_user: User = Depends(auth_service.get_current_user), db: AsyncSession = Depends(get_db)
):
    """
    The create_picture_rating function creates a new rating for the picture with the given id.
        The function takes in an integer representing the picture_id, an integer representing
        the rating, and a current_user object that is used to get information about who created
        this rating. It also takes in a database session object that is used to create and commit
        changes to our database.

    :param picture_id: int: Identify the picture to be rated
    :param rating: int: Set the rating value for a picture
    :param current_user: User: Get the user that is currently logged in
    :param db: AsyncSession: Pass the database session to the repository layer
    :return: A dictionary with two keys: rating and detail
    """
    if not (1 <= rating <= 5):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.get_message("RATING_MUST_BE_1_TO_5"))
    rating_picture = await repository_rating.create_picture_rating(picture_id, rating, current_user, db)

    return {"rating": rating_picture, "detail": messages.get_message("RATING_SUCCESSFULLY_ADDED")}


@router.get("{picture_id}/ratings", dependencies=[Depends(admin_moderator_user)], response_model=AverageRatingResponse)
async def picture_ratings(picture_id: int, db: AsyncSession = Depends(get_db)):
    """
    The picture_ratings function returns a list of ratings for the picture with the given id.
        If no such picture exists, it raises an HTTPException with status code 404 and detail &quot;Picture not found!&quot;.

    :param picture_id: int: Get the picture id from the url
    :param db: AsyncSession: Pass the database connection to the function
    :return: A list of ratings for a picture
    """
    picture = await repository_rating.picture_ratings(picture_id, db)
    if not picture:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.get_message("PICTURE_NOT_FOUND"))
    return picture


@router.delete("{picture_id}/ratings_delete", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(admin)])
async def remove_photo_rating(
    picture_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    The remove_photo_rating function is used to remove a rating from the database.
        It takes in a picture_id and user_id as parameters, and returns the deleted rating.

    :param picture_id: int: Get the picture id of the photo that is being rated
    :param user_id: int: Identify the user who is rating the photo
    :param db: AsyncSession: Get the database connection

    :return: The deleted rating
    """

    deleted_rating = await repository_rating.remove_rating(picture_id, user_id, db)
    if not deleted_rating:
        raise HTTPException(status_code=400, detail=messages.get_message("UNABLE_DELETE_RATING"))
    return deleted_rating
