"""Apply pending db/changes files in order: python tools/apply.py"""
import os
import re
from pathlib import Path

from neo4j import GraphDatabase

ROOT = Path(__file__).resolve().parent.parent


def main():
    driver = GraphDatabase.driver(os.environ["NEO4J_URI"], auth=(os.environ["NEO4J_USER"], os.environ["NEO4J_PASSWORD"]))
    with driver.session() as s:
        done = {r["name"] for r in s.run("MATCH (c:__Change) RETURN c.name AS name")}
        for path in sorted((ROOT / "db" / "changes").glob("*.cypher")):
            if path.name in done:
                continue
            for stmt in [x.strip() for x in re.split(r";\s*\n", path.read_text()) if x.strip()]:
                s.run(stmt).consume()          # auto-commit, so CALL { } IN TRANSACTIONS works
            s.run("CREATE (:__Change {name: $n, at: datetime()})", n=path.name).consume()
    driver.close()


if __name__ == "__main__":
    main()
