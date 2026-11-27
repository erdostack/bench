"""Publish procedure versions from procedures/*.yaml. The only writer to the database."""
import sys
from pathlib import Path

import yaml
from neo4j import GraphDatabase

MAX_STEPS = 40

CREATE_VERSION = """
CREATE (p:Procedure {id: $id, version: $version, title: $title})
WITH p
UNWIND range(0, size($steps) - 1) AS i
CREATE (s:Step {uid: $id + ':' + toString($version) + ':' + toString(i + 1), n: i + 1, text: $steps[i]})
WITH p, s
ORDER BY s.n
WITH p, collect(s) AS steps
WITH p, steps, steps[0] AS first
CREATE (p)-[:FIRST]->(first)
FOREACH (i IN range(0, size(steps) - 2) |
  FOREACH (a IN [steps[i]] |
    FOREACH (b IN [steps[i + 1]] |
      CREATE (a)-[:NEXT]->(b))))
"""

EXISTS = "MATCH (p:Procedure {id: $id, version: $version}) RETURN count(p) AS n"


def publish(session, doc):
    steps = [str(s) for s in doc["steps"]]
    if not 1 <= len(steps) <= MAX_STEPS:
        raise ValueError(f"{doc['id']} v{doc['version']}: {len(steps)} steps, must be 1 to {MAX_STEPS}")
    params = {"id": doc["id"], "version": int(doc["version"]), "title": doc["title"], "steps": steps}
    if session.run(EXISTS, params).single()["n"]:
        return False  # versions are immutable: already published
    session.execute_write(lambda tx: tx.run(CREATE_VERSION, params).consume())
    return True


def main(uri, user, password, folder="procedures"):
    with GraphDatabase.driver(uri, auth=(user, password)) as driver, driver.session() as session:
        for path in sorted(Path(folder).glob("*.yaml")):
            doc = yaml.safe_load(path.read_text())
            print(path.name, "published" if publish(session, doc) else "already published")


if __name__ == "__main__":
    main(*sys.argv[1:4])
