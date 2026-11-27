"""Driver handling. One driver per process."""
from functools import lru_cache

from neo4j import GraphDatabase, RoutingControl

from .settings import settings


@lru_cache(maxsize=1)
def driver():
    return GraphDatabase.driver(settings.graph_uri, auth=(settings.graph_user, settings.graph_password))


def read(query: str, **params) -> list[dict]:
    records, _, _ = driver().execute_query(query, params, routing_=RoutingControl.READ)
    return [record.data() for record in records]
