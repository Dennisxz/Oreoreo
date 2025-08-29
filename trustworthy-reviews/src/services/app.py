from fastapi import FastAPI
from service.schemas import ScoreRequest
from pipeline.score import score_one

app = FastAPI(title="Trustworthy Reviews API")

@app.post("/score_review")
def score_review(req: ScoreRequest):
    return score_one(req.review.dict(), req.place.dict())