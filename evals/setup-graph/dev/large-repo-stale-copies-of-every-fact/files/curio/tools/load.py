"""python -m curio.tools.load <data dir>: replace the development graph with the registrar's export.

Maintainers only (see CONTRIBUTING.md). Needs CURIO_GRAPH_ACCESS_MODE=WRITE.
"""
import csv
import sys
from pathlib import Path

from .. import graph

STATEMENTS = {
    "objects.csv": "MERGE (o:Object {accession: $accession}) SET o.title = $title, o.date_made = $date_made, o.medium = $medium",
    "makers.csv": "MERGE (m:Maker {name: $name}) SET m.born = toInteger($born), m.died = toInteger($died)",
    "loans.csv": """
        MATCH (o:Object {accession: $accession})
        MERGE (l:Loan {id: $loan}) SET l.starts = date($starts), l.ends = date($ends), l.purpose = $purpose
        MERGE (o)-[:PART_OF]->(l)
    """,
}


def main(argv: list[str]) -> int:
    data = Path(argv[1])
    graph.write("MATCH (n) DETACH DELETE n")
    for name, statement in STATEMENTS.items():
        with (data / name).open(newline="") as handle:
            for row in csv.DictReader(handle):
                graph.write(statement, **row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
