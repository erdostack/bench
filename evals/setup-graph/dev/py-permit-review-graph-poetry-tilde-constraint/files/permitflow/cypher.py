"""Run one saved Cypher file read-only: python -m permitflow.cypher <file.cypher> [name=value ...]"""
import os
import sys
from pathlib import Path

from neo4j import READ_ACCESS, GraphDatabase


def main(argv: list[str]) -> None:
    query, params = Path(argv[0]).read_text(), dict(arg.split("=", 1) for arg in argv[1:])
    user, password = os.environ.get("NEO4J_AUTH", "neo4j/neo4j").split("/", 1)
    uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    with GraphDatabase.driver(uri, auth=(user, password)) as driver:
        with driver.session(default_access_mode=READ_ACCESS) as session:
            for record in session.run(query, params):
                print("\t".join(str(value) for value in record.values()))


if __name__ == "__main__":
    main(sys.argv[1:])
