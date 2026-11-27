import json
import os
import sys
from pathlib import Path

from neo4j import GraphDatabase

STATEMENT = (Path(__file__).parent / "load_offers.cypher").read_text()


def main(paths):
    with GraphDatabase.driver(os.environ["NEO4J_URI"], auth=("neo4j", os.environ["NEO4J_PASSWORD"])) as drv:
        with drv.session(database="procurement") as session:
            for p in paths:
                offers = json.loads(Path(p).read_text())["offers"]
                session.execute_write(lambda tx: tx.run(STATEMENT, offers=offers).consume())
                print("loaded", p, len(offers))


if __name__ == "__main__":
    main(sys.argv[1:])
