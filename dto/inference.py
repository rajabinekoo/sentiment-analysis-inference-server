from typing import List

from pydantic import BaseModel, constr, Field


class InferenceDTO(BaseModel):
    queries: List[constr(min_length=7)] = Field(..., min_items=1, max_items=10)


class InferenceResponse:
    def __init__(self, body: str, prediction: float):
        self.body = body
        self.prediction = prediction
