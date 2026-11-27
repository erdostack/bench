import json
import os
import sys
from pathlib import Path

from neo4j import GraphDatabase

statement, feed = Path(sys.argv[1]).read_text(), json.loads(Path(sys.argv[2]).read_text())
with GraphDatabase.driver(os.environ["NEO4J_URI"], auth=("neo4j", os.environ["NEO4J_PASSWORD"])) as d:
    with d.session(database="airnet") as s:
        s.execute_write(lambda tx: tx.run(statement, rows=feed["devices"]).consume())
