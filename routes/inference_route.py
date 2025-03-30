from fastapi import FastAPI

from dto.inference import InferenceDTO
from services.inference_service import sentiment_analysis_inference

base_route = "/inference"


def init_inference_route(app: FastAPI):
    @app.post(f"{base_route}")
    async def inference_sentiment_analysis_model(body: InferenceDTO):
        return sentiment_analysis_inference(body)
