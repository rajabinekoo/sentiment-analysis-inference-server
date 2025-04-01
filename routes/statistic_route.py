from fastapi import FastAPI

from database.cassandra import cassandra_database
from dto.statistic import StatisticReqDTO

base_route = "/statistics"


def init_statistics_route(app: FastAPI):
    @app.get(f"{base_route}")
    async def list_of_statistics():
        return cassandra_database.get_statistics()

    @app.post(f"{base_route}")
    async def add_new_statistic(query: StatisticReqDTO):
        cassandra_database.add_statistic(query.key, query.value)
        return {"message": "Statistic added successfully"}

    @app.delete(f"{base_route}/" + "{key}")
    async def remove_statistic(key: str):
        cassandra_database.remove_statistic(key)
        return {"message": "Statistic removed successfully"}
