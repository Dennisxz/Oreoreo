from pydantic import BaseModel

class Place(BaseModel):
    id: str | None = None
    name: str | None = None
    category: str | None = None
    address: str | None = None

class Review(BaseModel):
    id: str | None = None
    text: str
    rating: float | None = None
    language: str | None = "en"

class ScoreRequest(BaseModel):
    place: Place
    review: Review
