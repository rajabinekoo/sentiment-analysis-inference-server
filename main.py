from fastapi import FastAPI
from bootstrap import bootstrap
from routes.inference_route import init_inference_route

bootstrap()
app = FastAPI()
init_inference_route(app)
