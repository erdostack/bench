"""One driver for the process; every saved query goes through read()."""
from functools import lru_cache
from pathlib import Path

from neo4j import GraphDatabase, RoutingControl

from . import settings

QUERIES = Path(__file__).resolve().parent.parent / "queries"


@lru_cache(maxsize=1)
def driver():
    cfg = settings.load()
    return GraphDatabase.driver(cfg.uri, auth=(cfg.user, cfg.password))


def read(text: str, **params):
    records, _, _ = driver().execute_query(text, params, routing_=RoutingControl.READ)
    return [record.data() for record in records]


def saved(name: str) -> str:
    return (QUERIES / f"{name}.cypher").read_text()
