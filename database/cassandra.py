import os
import base64

from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

from dto.review import GetReviewsDTO, ReviewDTO
from dto.statistic import StatisticResDTO
from libs.config import Configs


class CassandraDatabase:
    def __init__(self):
        cluster = Cluster([os.getenv('CASSANDRA_HOST')])
        self._session = cluster.connect()
        keyspace = os.getenv('CASSANDRA_KEYSPACE')
        self._session.set_keyspace(keyspace)
        self._session.execute(f"""
        CREATE TABLE IF NOT EXISTS {Configs.StatisticTable} (
            key text,
            value text,
            PRIMARY KEY (key)
        );
        """)

    def get_dataset(self, query: GetReviewsDTO):
        statement = SimpleStatement(f"""select * from {Configs.ReviewTable}""", fetch_size=query.limit)

        if query.cursor:
            paging_state = base64.b64decode(query.cursor)
            rows = self._session.execute(statement, paging_state=paging_state)
        else:
            rows = self._session.execute(statement)

        result = []
        for row in rows.current_rows:
            result.append(
                ReviewDTO(
                    body=row.body,
                    date=row.date,
                    user_id=row.user_id,
                    stars=int(row.stars),
                    review_id=row.review_id,
                    business_id=row.business_id,
                )
            )
        if not rows.has_more_pages:
            return result, None
        return result, base64.b64encode(rows.paging_state).decode()

    def add_statistic(self, key: str, value: str):
        rows = self._session.execute(f"SELECT * FROM {Configs.StatisticTable} WHERE key = '{key}'").all()
        if len(rows) == 0:
            self._session.execute(f"""INSERT INTO {Configs.StatisticTable} (key, value) VALUES ('{key}', '{value}');""")
        else:
            self._session.execute(f"UPDATE {Configs.StatisticTable} SET value = '{value}' WHERE key = '{key}';")

    def get_statistics(self) -> list[StatisticResDTO]:
        rows = self._session.execute(f"SELECT * FROM {Configs.StatisticTable}").all()
        if len(rows) == 0:
            return []
        result = []
        for row in rows:
            result.append(StatisticResDTO(row.key, row.value))
        return result

    def remove_statistic(self, key: str):
        self._session.execute(f"DELETE FROM {Configs.StatisticTable} WHERE key = '{key}'")


cassandra_database = CassandraDatabase()
