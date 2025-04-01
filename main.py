from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from bootstrap import bootstrap
from routes.review_route import init_review_route
from routes.inference_route import init_inference_route
from routes.statistic_route import init_statistics_route

bootstrap()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
init_review_route(app)
init_inference_route(app)
init_statistics_route(app)
