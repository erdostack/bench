"""The driver and the two ways of using it. Application code only ever calls read()."""
from functools import lru_cache
from pathlib import Path

from neo4j import READ_ACCESS, WRITE_ACCESS, GraphDatabase

from . import settings

QUERIES = Path(__file__).resolve().parent.parent / "queries"


@lru_cache(maxsize=1)
def driver():
    cfg = settings.load()
    return GraphDatabase.driver(cfg.uri, auth=(cfg.user, cfg.password))


def read(cypher: str, **params) -> list[dict]:
    cfg = settings.load()
    with driver().session(database=cfg.database, default_access_mode=READ_ACCESS) as session:
        return session.execute_read(lambda tx: [record.data() for record in tx.run(cypher, **params)])


def write(cypher: str, **params) -> None:
    """Used by curio.tools.load only."""
    cfg = settings.load()
    if cfg.access_mode != "WRITE":
        raise PermissionError("set CURIO_GRAPH_ACCESS_MODE=WRITE to run the loader")
    with driver().session(database=cfg.database, default_access_mode=WRITE_ACCESS) as session:
        session.execute_write(lambda tx: tx.run(cypher, **params).consume())


def saved(name: str) -> str:
    return (QUERIES / f"{name}.cypher").read_text()
