from pydantic import BaseModel


class RatingBase(BaseModel):
    rating: int


class RatingCreate(RatingBase):
    user_id: int
    picture_id: int


class RatingDB(RatingBase):
    id: int
    user_id: int
    picture_id: int


class RatingResponse(BaseModel):
    rating: RatingDB
    detail: str


class AverageRatingResponse(BaseModel):
    rating_average: float
