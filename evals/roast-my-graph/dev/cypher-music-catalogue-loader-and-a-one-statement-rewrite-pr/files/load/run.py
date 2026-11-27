"""Nightly loader: runs every statement of catalogue.cypher, in order, for each batch of rows."""
import json
import re
import sys
from pathlib import Path

from neo4j import GraphDatabase

REQUIRED = {
    "upsert_artists": ["artist_mbid"],
    "upsert_releases": ["release_mbid"],
    "link_artists": ["artist_mbid", "release_mbid"],
    "link_labels": ["release_mbid", "label_mbid"],
}


def statements(path):
    text = Path(path).read_text(encoding="utf-8")
    for name, body in re.findall(r"// name: (\w+)\n(.*?);", text, flags=re.S):
        yield name, body


def main(changes_file, uri, auth, batch=10000):
    rows = [json.loads(line) for line in open(changes_file, encoding="utf-8")]
    driver = GraphDatabase.driver(uri, auth=auth)
    skipped = {}
    with driver.session() as session:
        for start in range(0, len(rows), batch):
            chunk = rows[start:start + batch]
            for name, body in statements(Path(__file__).with_name("catalogue.cypher")):
                usable = [r for r in chunk if all(r.get(k) for k in REQUIRED[name])]
                skipped[name] = skipped.get(name, 0) + len(chunk) - len(usable)
                session.execute_write(lambda tx: tx.run(body, rows=usable).consume())
    print("skipped rows:", skipped)
    driver.close()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], (sys.argv[3], sys.argv[4]))
