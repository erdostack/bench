"""Connection to the graph backend. Auth is off in the local container."""
import os

from neo4j import GraphDatabase

driver = GraphDatabase.driver(os.environ.get("GRAPH_URI", "bolt://localhost:7687"), auth=("", ""))


def rows(query: str, **params) -> list[dict]:
    records, _, _ = driver.execute_query(query, params)
    return [r.data() for r in records]
