import base64
from typing import Optional
from pydantic import BaseModel, field_validator, Field, conint


class GetReviewsDTO(BaseModel):
    cursor: Optional[str] = Field(default=None)
    limit: Optional[conint(ge=1, le=100)] = Field(default=10)

    @field_validator('cursor')
    @classmethod
    def validate_cursor(cls, v):
        if v is None:
            return v
        try:
            base64.b64decode(v)
        except Exception:
            raise ValueError("Cursor must be a base64 string")
        return v


class ReviewDTO:
    def __init__(self, review_id: str, business_id: str, user_id: str, date: str, body: str, stars: int):
        self.review_id = review_id
        self.business_id = business_id
        self.user_id = user_id
        self.date = date
        self.body = body
        self.stars = stars
