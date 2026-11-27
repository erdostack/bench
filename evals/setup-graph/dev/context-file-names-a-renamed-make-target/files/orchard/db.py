"""Driver and a read helper."""
import os
from functools import lru_cache

from neo4j import GraphDatabase


@lru_cache(maxsize=1)
def driver():
    return GraphDatabase.driver(os.environ.get("ORCHARD_GRAPH_URI", "bolt://localhost:7687"),
                                auth=("neo4j", os.environ["ORCHARD_GRAPH_PASSWORD"]))


def read(query: str, **params) -> list[dict]:
    records, _, _ = driver().execute_query(query, params, routing_="r")
    return [r.data() for r in records]
