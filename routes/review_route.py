from fastapi import FastAPI, Depends

from database.cassandra import cassandra_database
from dto.review import GetReviewsDTO

base_route = "/review"


def init_review_route(app: FastAPI):
    @app.get(f"{base_route}")
    async def list_of_reviews(query: GetReviewsDTO = Depends(GetReviewsDTO)):
        reviews, cursor = cassandra_database.get_dataset(query)
        return {"list": reviews, "cursor": cursor}
