import os

from neo4j import GraphDatabase

_driver = None


def driver():
    global _driver
    if _driver is None:
        _driver = GraphDatabase.driver(os.environ["NEO4J_URI"], auth=("neo4j", os.environ["NEO4J_PASSWORD"]))
    return _driver
