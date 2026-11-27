"""python -m orchard.tools.import_register <dir>: merge the planting register into the graph. Writes."""
import csv
import sys
from pathlib import Path

from ..db import driver

if __name__ == "__main__":
    register = Path(sys.argv[1])
    with driver().session() as session:
        for row in csv.DictReader((register / "trees.csv").open()):
            session.run("MERGE (v:Variety {name: $variety}) MERGE (r:Row {name: $row}) "
                        "MERGE (t:Tree {tag: $tag}) SET t.planted = toInteger($planted) "
                        "MERGE (t)-[:OF_VARIETY]->(v) MERGE (t)-[:IN_ROW]->(r)", **row)
        for row in csv.DictReader((register / "grafts.csv").open()):
            session.run("MATCH (t:Tree {tag: $tree}), (s:Tree {tag: $scion_from}) MERGE (t)-[:SCION_FROM]->(s)", **row)
